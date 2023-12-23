function drawPoint(ctx, x, y, rotation, scaleX, scaleY, strokeStyle, lineWidth) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rotation);
  ctx.scale(scaleX, scaleY);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.arc(0, 0, lineWidth / 2, 0, 2 * Math.PI, false);
  ctx.fillStyle = strokeStyle;
  ctx.fill();
  ctx.restore();
}

function drawLineSegment(ctx, x1, y1, x2, y2, strokeStyle, lineWidth, lineCap='round') {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = strokeStyle;
  ctx.lineWidth = lineWidth;
  ctx.lineCap = lineCap;
  ctx.stroke();
}

function drawLine(ctx, x1, y1, x2, y2, rotation, scaleX, scaleY, strokeStyle, lineWidth, lineCap) {
  ctx.save();
  ctx.translate(x1, y1);
  ctx.rotate(rotation);
  ctx.scale(scaleX, scaleY);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(x2 - x1, y2 - y1);
  ctx.strokeStyle = strokeStyle;
  ctx.lineWidth = lineWidth;
  ctx.lineCap = lineCap;
  ctx.stroke();
  ctx.restore();
}

function drawEllipse(ctx, x, y, radiusX, radiusY, rotation, scaleX, scaleY, fillStyle, strokeStyle, lineWidth) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rotation);
  ctx.scale(scaleX, scaleY);
  ctx.beginPath();
  ctx.ellipse(radiusX, radiusY, radiusX, radiusY, 0, 0, 2 * Math.PI);
  ctx.fillStyle = fillStyle;
  ctx.fill();
  ctx.strokeStyle = strokeStyle;
  ctx.lineWidth = lineWidth;
  ctx.stroke();
  ctx.restore();
}

function drawRectangle(ctx, x, y, width, height, rotation, scaleX, scaleY, fillStyle, strokeStyle, lineWidth) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rotation);
  ctx.scale(scaleX, scaleY);
  ctx.fillStyle = fillStyle;
  ctx.strokeStyle = strokeStyle;
  ctx.lineWidth = lineWidth;
  ctx.beginPath();
  ctx.rect(0, 0, width, height);
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

function drawText(ctx, x, y, text, width, height, rotation, scaleX, scaleY, fillStyle, fontStyle, fontSize, fontFamily) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rotation);
  ctx.scale(scaleX, scaleY);
  ctx.fillStyle = fillStyle;
  ctx.font = `${fontStyle} ${fontSize}px ${fontFamily}`;
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, fontSize / 2);
  ctx.restore();
}

function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
}

function drawAnnotationsOnCanvas(designState, imageWidth, imageHeight) {

  const canvas = document.createElement('canvas');
  canvas.width = imageWidth;
  canvas.height = imageHeight;
  const showWidth = designState.shownImageDimensions.width;
  const showHeight = designState.shownImageDimensions.height;

  const ctx = canvas.getContext('2d');

  ctx.fillStyle = 'rgba(0, 0, 0, 0)';
  ctx.fillRect(0, 0, imageWidth, imageHeight);

  Object.keys(designState.annotations).forEach((key) => {
    const annotation = designState.annotations[key];
    const strokeStyle = annotation.stroke;
    const lineWidth = annotation.strokeWidth / showWidth * imageWidth;
    const opacity = annotation.opacity;

    //const strokeColor = hexToRGBA(strokeStyle, opacity);
    const strokeColor = hexToRGBA("#FFFFFF", 1.0);
    const fillColor = hexToRGBA("#FFFFFF", 1.0);

    const rotation = degreesToRadians(annotation.rotation || 0);
    const scaleX = annotation.scaleX || 1;
    const scaleY = annotation.scaleY || 1;


    if (annotation.name.toLowerCase() === "pen") {
      const points = annotation.points;
      if (points.length === 2) {
        drawPoint(
          ctx,
          points[0] / showWidth * imageWidth,
          points[1] / showHeight * imageHeight,
          rotation,
          scaleX,
          scaleY,
          strokeColor,
          lineWidth);
      } else {
        ctx.save();
        if (rotation !== 0) {
          ctx.translate(annotation.x / showWidth * imageWidth, annotation.y / showHeight * imageHeight);
          ctx.rotate(rotation);
        }
        ctx.scale(scaleX, scaleY);
        for (let i = 0; i < points.length - 2; i += 2) {
          drawLineSegment(
            ctx,
            points[i] / showWidth * imageWidth,
            points[i + 1] / showHeight * imageHeight,
            points[i + 2] / showWidth * imageWidth,
            points[i + 3] / showHeight * imageHeight,
            strokeColor,
            lineWidth);
        }
        ctx.restore();
      }
    } else if (annotation.name.toLowerCase() === "line") {
      drawLine(
        ctx,
        annotation.x / showWidth * imageWidth,
        annotation.y / showHeight * imageHeight,
        (annotation.x + annotation.points[2]) / showWidth * imageWidth,
        (annotation.y + annotation.points[3]) / showHeight * imageHeight,
        rotation,
        scaleX,
        scaleY,
        strokeColor,
        lineWidth);
    } else if (annotation.name.toLowerCase() === "ellipse") {
      drawEllipse(
        ctx,
        annotation.x / showWidth * imageWidth,
        annotation.y / showHeight * imageHeight,
        annotation.radiusX / showWidth * imageWidth,
        annotation.radiusY / showHeight * imageHeight,
        rotation,
        scaleX,
        scaleY,
        fillColor,
        strokeColor,
        lineWidth);
    } else if (annotation.name.toLowerCase() === "rect") {
      drawRectangle(
        ctx,
        annotation.x / showWidth * imageWidth,
        annotation.y / showHeight * imageHeight,
        annotation.width / showWidth * imageWidth,
        annotation.height / showHeight * imageHeight,
        rotation,
        scaleX,
        scaleY,
        fillColor,
        strokeColor,
        lineWidth);
    } else if (annotation.name.toLowerCase() === "text") {
      drawText(
        ctx,
        annotation.x / showWidth * imageWidth,
        annotation.y / showHeight * imageHeight,
        annotation.text,
        annotation.width / showWidth * imageWidth,
        annotation.height / showHeight * imageHeight,
        rotation,
        scaleX,
        scaleY,
        strokeColor,
        annotation.fontStyle,
        annotation.fontSize / showHeight * imageHeight,
        annotation.fontFamily);
    }
  });

  // Return the canvas element
  return canvas;
}

// Helper function to convert hex color and opacity to rgba
function hexToRGBA(hex, opacity) {
  let shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  hex = hex.replace(shorthandRegex, function(m, r, g, b) {
    return r + r + g + g + b + b;
  });

  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? `rgba(${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}, ${opacity})` : null;
}
