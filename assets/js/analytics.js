/**
 * Analytics Module for GTM DataLayer Event Tracking
 *
 * Central hub for pushing events to Google Tag Manager's dataLayer.
 * All tracking should go through this module to ensure consistent
 * event structure and prevent duplicates.
 *
 * Usage:
 *   Analytics.trackLinkClick(url, text, type, category);
 *   Analytics.trackScroll(depth);
 *   Analytics.trackButtonClick(text, category);
 *   Analytics.trackFormSubmit(formName, status);
 *   Analytics.trackComponentInteraction(name, action, data);
 */

const Analytics = (() => {
  'use strict';

  /**
   * Push event to dataLayer with consistent structure
   * @private
   * @param {string} eventName - Name of the event (e.g., 'link_click')
   * @param {object} data - Event data (properties will be merged into event)
   */
  function pushEvent(eventName, data = {}) {
    window.dataLayer = window.dataLayer || [];

    const event = {
      event: eventName,
      timestamp: new Date().toISOString(),
      ...data
    };

    window.dataLayer.push(event);

    // Debug logging (can be disabled in production if needed)
    if (typeof console !== 'undefined' && console.debug) {
      console.debug(`[Analytics] Event: ${eventName}`, event);
    }
  }

  /**
   * Track link click with full context
   * @param {string} url - Link href
   * @param {string} text - Link text content
   * @param {string} type - Link type: 'nav', 'blog', 'services', 'internal', 'external'
   * @param {string} category - Link category for grouping (e.g., 'navigation', 'post-body')
   */
  function trackLinkClick(url, text, type, category = '') {
    pushEvent('link_click', {
      click_url: url,
      click_text: text,
      link_type: type,
      link_category: category
    });
  }

  /**
   * Track button click (CTAs, form buttons, etc.)
   * @param {string} text - Button text content
   * @param {string} category - Button category (e.g., 'contact-cta', 'form-submit')
   */
  function trackButtonClick(text, category = '') {
    pushEvent('button_click', {
      click_text: text,
      button_category: category
    });
  }

  /**
   * Track scroll depth milestone
   * @param {number} depth - Scroll depth percentage (25, 50, 75, 100)
   */
  function trackScroll(depth) {
    pushEvent('scroll_depth', {
      scroll_depth: depth
    });
  }

  /**
   * Track form interaction (submit, error, etc.)
   * @param {string} formName - Name/identifier of the form
   * @param {string} status - Status: 'start', 'success', 'error'
   * @param {object} data - Additional form data (optional)
   */
  function trackFormSubmit(formName, status, data = {}) {
    pushEvent('form_interaction', {
      form_name: formName,
      interaction_type: 'submit',
      form_status: status,
      ...data
    });
  }

  /**
   * Track component interaction (carousel, accordion, etc.)
   * @param {string} componentName - Name of component (e.g., 'testimonials', 'toc')
   * @param {string} action - Action performed (e.g., 'navigate', 'expand', 'click')
   * @param {object} data - Additional interaction data
   */
  function trackComponentInteraction(componentName, action, data = {}) {
    pushEvent('component_interaction', {
      component_name: componentName,
      interaction_type: action,
      ...data
    });
  }

  // Public API
  return {
    trackLinkClick,
    trackButtonClick,
    trackScroll,
    trackFormSubmit,
    trackComponentInteraction
  };
})();
