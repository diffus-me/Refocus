import json
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


class MonitorException(Exception):
    def __init__(self, task_id: str, status_code: int, msg: str):
        self.task_id = task_id
        self.status_code = status_code
        self._msg = msg

    def __repr__(self) -> str:
        return self._msg


class MonitorTierMismatchedException(Exception):
    def __init__(self, msg, current_tier, allowed_tiers):
        self._msg = msg
        self.current_tier = current_tier
        self.allowed_tiers = allowed_tiers

    def __repr__(self) -> str:
        return self._msg


def _get_system_monitor_config(request_headers: dict):
    monitor_addr = request_headers.get('x-diffus-system-monitor-url', '') or request_headers.get(
        'X-Diffus-System-Monitor-Url', '')
    system_monitor_api_secret = request_headers.get('x-diffus-system-monitor-api-secret', '') or request_headers.get(
        'X-Diffus-System-Monitor-Api-Secret', '')
    if not monitor_addr or not system_monitor_api_secret:
        monitor_addr = os.getenv('SYSTEM_MONITOR_ADDR')
        system_monitor_api_secret = os.getenv('SYSTEM_MONITOR_API_SECRET')
    return monitor_addr, system_monitor_api_secret


async def _before_task_started(
        session: aiohttp.ClientSession,
        request_headers: dict,
        api_name: str,
        function_name: str,
        job_id: Optional[str] = None,
        decoded_params: Optional[dict] = None,
        is_intermediate: bool = False,
        refund_if_task_failed: bool = True,
        only_available_for: Optional[list[str]] = None) -> Optional[str]:
    if job_id is None:
        job_id = str(uuid.uuid4())
    monitor_addr, system_monitor_api_secret = _get_system_monitor_config(request_headers)
    if not monitor_addr or not system_monitor_api_secret:
        logger.error(f'{job_id}: system_monitor_addr or system_monitor_api_secret is not present')
        return None

    session_hash = request_headers.get('x-session-hash', None)
    if not session_hash:
        logger.error(f'{job_id}: x-session-hash does not presented in headers')
        return None
    task_id = request_headers.get('x-task-id', None)
    if not task_id:
        logger.error(f'{job_id}: x-task-id does not presented in headers')
        return None
    if not is_intermediate and task_id != job_id:
        logger.error(f'x-task-id ({task_id}) and job_id ({job_id}) are not equal')
    deduct_flag = request_headers.get('x-deduct-credits', None)
    deduct_flag = not (deduct_flag == 'false')
    if only_available_for:
        user_tier = request_headers.get('user-tire', None) or request_headers.get('user-tier', None)
        if not user_tier or user_tier.lower() not in [item.lower() for item in only_available_for]:
            raise MonitorTierMismatchedException(
                f'This feature is available for {only_available_for} only. The current user tier is {user_tier}.',
                user_tier,
                only_available_for)

    user_id = request_headers.get('user-id', 'local')
    request_data = {
        'api': api_name,
        'initiator': function_name,
        'user': user_id,
        'started_at': time.time(),
        'session_hash': session_hash,
        'skip_charge': not deduct_flag,
        'refund_if_task_failed': refund_if_task_failed,
        'node': os.getenv('HOST_IP', default=''),
    }
    if is_intermediate:
        request_data['step_id'] = job_id
        request_data['task_id'] = task_id
    else:
        request_data['task_id'] = job_id
    if decoded_params:
        request_data['decoded_params'] = decoded_params
    async with session.post(monitor_addr,
                            headers={
                                'Api-Secret': system_monitor_api_secret,
                            },
                            json=request_data) as resp:
        logger.info(json.dumps(request_data, ensure_ascii=False, sort_keys=True))

        # check response, raise exception if status code is not 2xx
        if 199 < resp.status < 300:
            return job_id

        # log the response if request failed
        resp_text = await resp.text()
        logger.error(
            f'create monitor log failed, status: {resp.status}, message: {resp_text[:min(100, len(resp_text))]}'
        )
        raise MonitorException(task_id, resp.status, resp_text)


async def _after_task_finished(
        session: aiohttp.ClientSession,
        request_headers: dict,
        job_id: Optional[str],
        status: str,
        message: Optional[str] = None,
        is_intermediate: bool = False,
        refund_if_failed: bool = False):
    if job_id is None:
        logger.error(
            'task_id is not present in after_task_finished, there might be error occured in before_task_started.')
        return
    monitor_addr, system_monitor_api_secret = _get_system_monitor_config(request_headers)
    if not monitor_addr or not system_monitor_api_secret:
        logger.error(f'{job_id}: system_monitor_addr or system_monitor_api_secret is not present')
        return

    session_hash = request_headers.get('x-session-hash', None)
    if not session_hash:
        logger.error(f'{job_id}: x-session-hash does not presented in headers')
        return None
    task_id = request_headers.get('x-task-id', None)
    if not task_id:
        logger.error(f'{job_id}: x-task-id does not presented in headers')
        return None

    request_url = f'{monitor_addr}/{job_id}'
    request_body = {
        'status': status,
        'result': message if message else "{}",
        'finished_at': time.time(),
        'session_hash': session_hash,
        'refund_if_failed': refund_if_failed,
    }
    if is_intermediate:
        request_body['step_id'] = job_id
        request_body['task_id'] = task_id
    else:
        request_body['task_id'] = job_id
    async with session.post(request_url,
                            headers={
                                'Api-Secret': system_monitor_api_secret,
                            },
                            json=request_body) as resp:
        # log the response if request failed
        if resp.status < 200 or resp.status > 299:
            resp_text = await resp.text()
            logger.error((f'update monitor log failed, status: monitor_log_id: {job_id}, {resp.status}, '
                          f'message: {resp_text[:min(100, len(resp_text))]}'))


@asynccontextmanager
async def monitor_call_context(
        request_headers: dict,
        api_name: str,
        function_name: str,
        task_id: Optional[str] = None,
        decoded_params: Optional[dict] = None,
        is_intermediate: bool = True,
        refund_if_task_failed: bool = True,
        refund_if_failed: bool = False,
        only_available_for: Optional[list[str]] = None,
):
    status = 'unknown'
    message = ''
    task_is_failed = False

    def result_encoder(result, task_failed=False):
        try:
            nonlocal message
            nonlocal task_is_failed
            message = json.dumps(result, ensure_ascii=False, sort_keys=True)
            task_is_failed = task_failed
        except Exception as e:
            logger.error(f'{task_id}: Json encode result failed {str(e)}.')

    async with aiohttp.ClientSession() as session:
        try:
            task_id = await _before_task_started(
                session,
                request_headers,
                api_name,
                function_name,
                task_id,
                decoded_params,
                is_intermediate,
                refund_if_task_failed,
                only_available_for)
            yield result_encoder
            if task_is_failed:
                status = 'failed'
            else:
                status = 'finished'
        except Exception as e:
            status = 'failed'
            message = f'{type(e).__name__}: {str(e)}'
            raise e
        finally:
            await _after_task_finished(session,
                                       request_headers,
                                       task_id,
                                       status,
                                       message,
                                       is_intermediate,
                                       refund_if_failed)
