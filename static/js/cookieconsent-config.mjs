import "https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@v3.0.0/dist/cookieconsent.umd.js";

function popCookieConsent() {
  CookieConsent.run({
    categories: {
      necessary: {
        enabled: true,
        readOnly: true,
      },
      analytics: {
        enabled: true,
      },
      advertising: {
        enabled: true,
      },
    },
    language: {
      default: "en",
      translations: {
        en: {
          consentModal: {
            title: "Cookies Make Everything Better!",
            description:
              "Just like a warm batch of cookies straight out of the oven, our website uses its own cookies to ensure everything works perfectly for you. We’d also love to use additional cookies for analytics and ads to make your experience even yummier! Can we tempt you to share a bit more with us?",
            acceptAllBtn: "Accept all",
            showPreferencesBtn: "Pick my own",
            footer: `
                <a href="https://www.diffus.graviti.com/privacy" target="_blank">Privacy Policy</a>
                <a href="https://www.diffus.graviti.com/terms" target="_blank">Terms and Conditions</a>
                `,
          },
          preferencesModal: {
            title: "Your Cookie Tray",
            acceptAllBtn: "Accept all",
            acceptNecessaryBtn: "Only essentials",
            savePreferencesBtn: "Save my cookie choice",
            closeIconLabel: "Close this menu",
            sections: [
              {
                title: "The Secret Ingredient!",
                description:
                  "Our secret ingredient is your preferences. Help us tailor your experience to your taste!",
              },
              {
                title: "Strictly Necessary cookies",
                description:
                  "These cookies are like the flour in cookie dough – absolutely essential. They’re needed for the website to function and can’t be switched off. They work behind the scenes to keep your visit smooth and secure.",
                linkedCategory: "necessary",
              },
              {
                title: "Performance and Analytics Cookies",
                description:
                  "These cookies help us understand how visitors interact with our website, like a chef perfecting a recipe. They give us the scoop on which pages are most popular and how you whisk through our content, all while keeping your information anonymous.",
                linkedCategory: "analytics",
              },
              {
                title: "Marketing Cookies",
                description:
                  "Fancy some special offers? With these cookies, ads can be tailored to be as tempting as a chocolate chip right when you crave it. They help us serve up the content that’s most relevant to you.",
                linkedCategory: "advertising",
              },
              {
                title: "Need More Info?",
                description:
                  'If you’re curious about our cookie policy or have any questions, don’t hesitate to <a href="mailto:contact@graviti.com">drop us a line</a>. We’re here to help and chat – preferably over cookies!',
              },
            ],
          },
        },
      },
    },
    onConsent: function() {
      let adAnalyticsStorageConsent = "denied";
      if (CookieConsent.acceptedCategory("analytics")) {
        adAnalyticsStorageConsent = "granted";
      }
      let adStorageConsent = "denied";
      let adUserDataConsent = "denied";
      let adPersonalizationConsent = "denied";
      if (CookieConsent.acceptedCategory("advertising")) {
        adStorageConsent = "granted";
        adUserDataConsent = "granted";
        adPersonalizationConsent = "granted";
      }
      gtag("consent", "update", {
        ad_storage: adStorageConsent,
        ad_user_data: adUserDataConsent,
        ad_personalization: adPersonalizationConsent,
        analytics_storage: adAnalyticsStorageConsent,
        wait_for_update: 500,
      });
      gtag("set", "ads_data_redaction", true);
      Cookies.set("_ad_consent_ad_storage", adStorageConsent, { expires: 730 });
      Cookies.set("_ad_consent_user_data", adUserDataConsent, { expires: 730 });
      Cookies.set("_ad_consent_personalization", adPersonalizationConsent, {
        expires: 730,
      });
      Cookies.set("_ad_consent_analytics_storage", adAnalyticsStorageConsent, {
        expires: 730,
      });
    },
    onChange: function({ changedCategories, changedServices }) {
      let adStorageConsent = Cookies.get("_ad_consent_ad_storage");
      let adUserDataConsent = Cookies.get("_ad_consent_user_data");
      let adPersonalizationConsent = Cookies.get("_ad_consent_personalization");
      let adAnalyticsStorageConsent = Cookies.get(
        "_ad_consent_analytics_storage",
      );
      if (changedCategories.includes("analytics")) {
        if (CookieConsent.acceptedCategory("analytics")) {
          adAnalyticsStorageConsent = "granted";
        } else {
          adAnalyticsStorageConsent = "denied";
        }
        Cookies.set(
          "_ad_consent_analytics_storage",
          adAnalyticsStorageConsent,
          { expires: 730 },
        );
      }
      if (changedCategories.includes("advertising")) {
        if (CookieConsent.acceptedCategory("advertising")) {
          adStorageConsent = "granted";
          adUserDataConsent = "granted";
          adPersonalizationConsent = "granted";
        } else {
          adStorageConsent = "denied";
          adUserDataConsent = "denied";
          adPersonalizationConsent = "denied";
        }
        Cookies.set("_ad_consent_ad_storage", adStorageConsent, {
          expires: 730,
        });
        Cookies.set("_ad_consent_user_data", adUserDataConsent, {
          expires: 730,
        });
        Cookies.set("_ad_consent_personalization", adPersonalizationConsent, {
          expires: 730,
        });
      }
      gtag("consent", "update", {
        ad_storage: adStorageConsent,
        ad_user_data: adUserDataConsent,
        ad_personalization: adPersonalizationConsent,
        analytics_storage: adAnalyticsStorageConsent,
        wait_for_update: 500,
      });
      gtag("set", "ads_data_redaction", true);
    },
  });
}

if (window === window.top) {
  popCookieConsent();
} else {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const paramValue = urlParams.get('cookie_consent');
  if (paramValue === "true") {
    popCookieConsent();
  }
}
