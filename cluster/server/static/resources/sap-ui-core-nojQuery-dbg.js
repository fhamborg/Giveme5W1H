/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

/**
 * Device and Feature Detection API: Provides information about the used browser / device and cross platform support for certain events
 * like media queries, orientation change or resizing.
 *
 * This API is independent from any other part of the UI5 framework. This allows it to be loaded beforehand, if it is needed, to create the UI5 bootstrap
 * dynamically depending on the capabilities of the browser or device.
 *
 * @version 1.46.7
 * @namespace
 * @name sap.ui.Device
 * @public
 */

/*global console */

//Declare Module if API is available
if (window.jQuery && window.jQuery.sap && window.jQuery.sap.declare) {
	window.jQuery.sap.declare("sap.ui.Device", false);
}

//Introduce namespace if it does not yet exist
if (typeof window.sap !== "object" && typeof window.sap !== "function" ) {
	  window.sap = {};
}
if (typeof window.sap.ui !== "object") {
	window.sap.ui = {};
}

(function() {
	"use strict";

	//Skip initialization if API is already available
	if (typeof window.sap.ui.Device === "object" || typeof window.sap.ui.Device === "function" ) {
		var apiVersion = "1.46.7";
		window.sap.ui.Device._checkAPIVersion(apiVersion);
		return;
	}

	var device = {};

////-------------------------- Logging -------------------------------------
	/* since we cannot use the logging from jquery.sap.global.js, we need to come up with a seperate
	 * solution for the device API
	 */
	// helper function for date formatting
	function pad0(i,w) {
		return ("000" + String(i)).slice(-w);
	}

	var FATAL = 0, ERROR = 1, WARNING = 2, INFO = 3, DEBUG = 4, TRACE = 5;

	var deviceLogger = function() {
		this.defaultComponent = 'DEVICE';
		this.sWindowName = (window.top == window) ? "" : "[" + window.location.pathname.split('/').slice(-1)[0] + "] ";
	// Creates a new log entry depending on its level and component.
		this.log = function (iLevel, sMessage, sComponent) {
			sComponent = sComponent || this.defaultComponent  || '';
				var oNow = new Date(),
					oLogEntry = {
						time     : pad0(oNow.getHours(),2) + ":" + pad0(oNow.getMinutes(),2) + ":" + pad0(oNow.getSeconds(),2),
						date     : pad0(oNow.getFullYear(),4) + "-" + pad0(oNow.getMonth() + 1,2) + "-" + pad0(oNow.getDate(),2),
						timestamp: oNow.getTime(),
						level    : iLevel,
						message  : sMessage || "",
						component: sComponent || ""
					};
				/*eslint-disable no-console */
				if (window.console) { // in IE and FF, console might not exist; in FF it might even disappear
					var logText = oLogEntry.date + " " + oLogEntry.time + " " + this.sWindowName + oLogEntry.message + " - " + oLogEntry.component;
					switch (iLevel) {
					case FATAL:
					case ERROR: console.error(logText); break;
					case WARNING: console.warn(logText); break;
					case INFO: console.info ? console.info(logText) : console.log(logText); break;    // info not available in iOS simulator
					case DEBUG: console.debug ? console.debug(logText) : console.log(logText); break; // debug not available in IE, fallback to log
					case TRACE: console.trace ? console.trace(logText) : console.log(logText); break; // trace not available in IE, fallback to log (no trace)
					}
				}
				/*eslint-enable no-console */
				return oLogEntry;
		};
	};
// instantiate new logger
	var logger = new deviceLogger();
	logger.log(INFO, "Device API logging initialized");


//******** Version Check ********

	//Only used internal to make clear when Device API is loaded in wrong version
	device._checkAPIVersion = function(sVersion){
		var v = "1.46.7";
		if (v != sVersion) {
			logger.log(WARNING, "Device API version differs: " + v + " <-> " + sVersion);
		}
	};


//******** Event Management ******** (see Event Provider)

	var mEventRegistry = {};

	function attachEvent(sEventId, fnFunction, oListener) {
		if (!mEventRegistry[sEventId]) {
			mEventRegistry[sEventId] = [];
		}
		mEventRegistry[sEventId].push({oListener: oListener, fFunction:fnFunction});
	}

	function detachEvent(sEventId, fnFunction, oListener) {
		var aEventListeners = mEventRegistry[sEventId];

		if (!aEventListeners) {
			return this;
		}

		for (var i = 0, iL = aEventListeners.length; i < iL; i++) {
			if (aEventListeners[i].fFunction === fnFunction && aEventListeners[i].oListener === oListener) {
				aEventListeners.splice(i,1);
				break;
			}
		}
		if (aEventListeners.length == 0) {
			delete mEventRegistry[sEventId];
		}
	}

	function fireEvent(sEventId, mParameters) {
		var aEventListeners = mEventRegistry[sEventId], oInfo;
		if (aEventListeners) {
			aEventListeners = aEventListeners.slice();
			for (var i = 0, iL = aEventListeners.length; i < iL; i++) {
				oInfo = aEventListeners[i];
				oInfo.fFunction.call(oInfo.oListener || window, mParameters);
			}
		}
	}

//******** OS Detection ********

	/**
	 * Contains information about the operating system of the device.
	 *
	 * @namespace
	 * @name sap.ui.Device.os
	 * @public
	 */
	/**
	 * Enumeration containing the names of known operating systems.
	 *
	 * @namespace
	 * @name sap.ui.Device.os.OS
	 * @public
	 */
	/**
	 * The name of the operating system.
	 *
	 * @see sap.ui.Device.os.OS
	 * @name sap.ui.Device.os.name
	 * @type String
	 * @public
	 */
	/**
	 * The version of the operating system as <code>string</code>.
	 *
	 * Might be empty if no version can be determined.
	 *
	 * @name sap.ui.Device.os.versionStr
	 * @type String
	 * @public
	 */
	/**
	 * The version of the operating system as <code>float</code>.
	 *
	 * Might be <code>-1</code> if no version can be determined.
	 *
	 * @name sap.ui.Device.os.version
	 * @type float
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, a Windows operating system is used.
	 *
	 * @name sap.ui.Device.os.windows
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, a Linux operating system is used.
	 *
	 * @name sap.ui.Device.os.linux
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, a Mac operating system is used.
	 *
	 * @name sap.ui.Device.os.macintosh
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, an iOS operating system is used.
	 *
	 * @name sap.ui.Device.os.ios
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, an Android operating system is used.
	 *
	 * @name sap.ui.Device.os.android
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, a Blackberry operating system is used.
	 *
	 * @name sap.ui.Device.os.blackberry
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, a Windows Phone operating system is used.
	 *
	 * @name sap.ui.Device.os.windows_phone
	 * @type boolean
	 * @public
	 */

	/**
	 * Windows operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.WINDOWS
	 * @public
	 */
	/**
	 * MAC operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.MACINTOSH
	 * @public
	 */
	/**
	 * Linux operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.LINUX
	 * @public
	 */
	/**
	 * iOS operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.IOS
	 * @public
	 */
	/**
	 * Android operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.ANDROID
	 * @public
	 */
	/**
	 * Blackberry operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.BLACKBERRY
	 * @public
	 */
	/**
	 * Windows Phone operating system name.
	 *
	 * @see sap.ui.Device.os.name
	 * @name sap.ui.Device.os.OS.WINDOWS_PHONE
	 * @public
	 */

	var OS = {
		"WINDOWS": "win",
		"MACINTOSH": "mac",
		"LINUX": "linux",
		"IOS": "iOS",
		"ANDROID": "Android",
		"BLACKBERRY": "bb",
		"WINDOWS_PHONE": "winphone"
	};

	function getOS(userAgent){ // may return null!!

		userAgent = userAgent || navigator.userAgent;

		var platform, // regular expression for platform
			result;

		function getDesktopOS(){
			var pf = navigator.platform;
			if (pf.indexOf("Win") != -1 ) {
				// userAgent in windows 7 contains: windows NT 6.1
				// userAgent in windows 8 contains: windows NT 6.2 or higher
				// userAgent since windows 10: Windows NT 10[...]
				var rVersion = /Windows NT (\d+).(\d)/i;
				var uaResult = userAgent.match(rVersion);
				var sVersionStr = "";
				if (uaResult[1] == "6") {
					if (uaResult[2] == 1) {
						sVersionStr = "7";
					} else if (uaResult[2] > 1) {
						sVersionStr = "8";
					}
				} else {
					sVersionStr = uaResult[1];
				}
				return {"name": OS.WINDOWS, "versionStr": sVersionStr};
			} else if (pf.indexOf("Mac") != -1) {
				return {"name": OS.MACINTOSH, "versionStr": ""};
			} else if (pf.indexOf("Linux") != -1) {
				return {"name": OS.LINUX, "versionStr": ""};
			}
			logger.log(INFO, "OS detection returned no result");
			return null;
		}

		// Windows Phone. User agent includes other platforms and therefore must be checked first:
		platform = /Windows Phone (?:OS )?([\d.]*)/;
		result = userAgent.match(platform);
		if (result) {
			return ({"name": OS.WINDOWS_PHONE, "versionStr": result[1]});
		}

		// BlackBerry 10:
		if (userAgent.indexOf("(BB10;") > 0) {
			platform = /\sVersion\/([\d.]+)\s/;
			result = userAgent.match(platform);
			if (result) {
				return {"name": OS.BLACKBERRY, "versionStr": result[1]};
			} else {
				return {"name": OS.BLACKBERRY, "versionStr": '10'};
			}
		}

		// iOS, Android, BlackBerry 6.0+:
		platform = /\(([a-zA-Z ]+);\s(?:[U]?[;]?)([\D]+)((?:[\d._]*))(?:.*[\)][^\d]*)([\d.]*)\s/;
		result = userAgent.match(platform);
		if (result) {
			var appleDevices = /iPhone|iPad|iPod/;
			var bbDevices = /PlayBook|BlackBerry/;
			if (result[0].match(appleDevices)) {
				result[3] = result[3].replace(/_/g, ".");
				//result[1] contains info of devices
				return ({"name": OS.IOS, "versionStr": result[3]});
			} else if (result[2].match(/Android/)) {
				result[2] = result[2].replace(/\s/g, "");
				return ({"name": OS.ANDROID, "versionStr": result[3]});
			} else if (result[0].match(bbDevices)) {
				return ({"name": OS.BLACKBERRY, "versionStr": result[4]});
			}
		}

		//Firefox on Android
		platform = /\((Android)[\s]?([\d][.\d]*)?;.*Firefox\/[\d][.\d]*/;
		result = userAgent.match(platform);
		if (result) {
			return ({"name": OS.ANDROID, "versionStr": result.length == 3 ? result[2] : ""});
		}

		// Desktop
		return getDesktopOS();
	}

	function setOS(customUA) {
		device.os = getOS(customUA) || {};
		device.os.OS = OS;
		device.os.version = device.os.versionStr ? parseFloat(device.os.versionStr) : -1;

		if (device.os.name) {
			for (var b in OS) {
				if (OS[b] === device.os.name) {
					device.os[b.toLowerCase()] = true;
				}
			}
		}
	}
	setOS();
	// expose for unit test
	device._setOS = setOS;



//******** Browser Detection ********

	/**
	 * Contains information about the used browser.
	 *
	 * @namespace
	 * @name sap.ui.Device.browser
	 * @public
	 */

	/**
	 * Enumeration containing the names of known browsers.
	 *
	 * @namespace
	 * @name sap.ui.Device.browser.BROWSER
	 * @public
	 */

	/**
	 * The name of the browser.
	 *
	 * @see sap.ui.Device.browser.BROWSER
	 * @name sap.ui.Device.browser.name
	 * @type String
	 * @public
	 */
	/**
	 * The version of the browser as <code>string</code>.
	 *
	 * Might be empty if no version can be determined.
	 *
	 * @name sap.ui.Device.browser.versionStr
	 * @type String
	 * @public
	 */
	/**
	 * The version of the browser as <code>float</code>.
	 *
	 * Might be <code>-1</code> if no version can be determined.
	 *
	 * @name sap.ui.Device.browser.version
	 * @type float
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the mobile variant of the browser is used or
	 * a tablet or phone device is detected.
	 *
	 * <b>Note:</b> This information might not be available for all browsers.
	 *
	 * @name sap.ui.Device.browser.mobile
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Microsoft Internet Explorer browser is used.
	 *
	 * @name sap.ui.Device.browser.internet_explorer
	 * @type boolean
	 * @deprecated since 1.20, use {@link sap.ui.Device.browser.msie} instead.
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Microsoft Internet Explorer browser is used.
	 *
	 * @name sap.ui.Device.browser.msie
	 * @type boolean
	 * @since 1.20.0
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Microsoft Edge browser is used.
	 *
	 * @name sap.ui.Device.browser.edge
	 * @type boolean
	 * @since 1.30.0
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Mozilla Firefox browser is used.
	 *
	 * @name sap.ui.Device.browser.firefox
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Google Chrome browser is used.
	 *
	 * @name sap.ui.Device.browser.chrome
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Apple Safari browser is used.
	 *
	 * <b>Note:</b>
	 * This flag is also <code>true</code> when the standalone (fullscreen) mode or webview is used on iOS devices.
	 * Please also note the flags {@link sap.ui.Device.browser.fullscreen} and {@link sap.ui.Device.browser.webview}.
	 *
	 * @name sap.ui.Device.browser.safari
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, a browser featuring a Webkit engine is used.
	 *
	 * @name sap.ui.Device.browser.webkit
	 * @type boolean
	 * @since 1.20.0
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Safari browser runs in standalone fullscreen mode on iOS.
	 *
	 * <b>Note:</b> This flag is only available if the Safari browser was detected. Furthermore, if this mode is detected,
	 * technically not a standard Safari is used. There might be slight differences in behavior and detection, e.g.
	 * the availability of {@link sap.ui.Device.browser.version}.
	 *
	 * @name sap.ui.Device.browser.fullscreen
	 * @type boolean
	 * @since 1.31.0
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Safari browser runs in webview mode on iOS.
	 *
	 * <b>Note:</b> This flag is only available if the Safari browser was detected. Furthermore, if this mode is detected,
	 * technically not a standard Safari is used. There might be slight differences in behavior and detection, e.g.
	 * the availability of {@link sap.ui.Device.browser.version}.
	 *
	 * @name sap.ui.Device.browser.webview
	 * @type boolean
	 * @since 1.31.0
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the Phantom JS browser is used.
	 *
	 * @name sap.ui.Device.browser.phantomJS
	 * @type boolean
	 * @private
	 */
	/**
	 * The version of the used Webkit engine, if available.
	 *
	 * @see sap.ui.Device.browser.webkit
	 * @name sap.ui.Device.browser.webkitVersion
	 * @type String
	 * @since 1.20.0
	 * @private
	 */
	/**
	 * If this flag is set to <code>true</code>, a browser featuring a Mozilla engine is used.
	 *
	 * @name sap.ui.Device.browser.mozilla
	 * @type boolean
	 * @since 1.20.0
	 * @public
	 */
	/**
	 * Internet Explorer browser name.
	 *
	 * @see sap.ui.Device.browser.name
	 * @name sap.ui.Device.browser.BROWSER.INTERNET_EXPLORER
	 * @public
	 */
	/**
	 * Edge browser name.
	 *
	 * @see sap.ui.Device.browser.name
	 * @name sap.ui.Device.browser.BROWSER.EDGE
	 * @since 1.28.0
	 * @public
	 */
	/**
	 * Firefox browser name.
	 *
	 * @see sap.ui.Device.browser.name
	 * @name sap.ui.Device.browser.BROWSER.FIREFOX
	 * @public
	 */
	/**
	 * Chrome browser name.
	 *
	 * @see sap.ui.Device.browser.name
	 * @name sap.ui.Device.browser.BROWSER.CHROME
	 * @public
	 */
	/**
	 * Safari browser name.
	 *
	 * @see sap.ui.Device.browser.name
	 * @name sap.ui.Device.browser.BROWSER.SAFARI
	 * @public
	 */
	/**
	 * Android stock browser name.
	 *
	 * @see sap.ui.Device.browser.name
	 * @name sap.ui.Device.browser.BROWSER.ANDROID
	 * @public
	 */

	var BROWSER = {
		"INTERNET_EXPLORER": "ie",
		"EDGE": "ed",
		"FIREFOX": "ff",
		"CHROME": "cr",
		"SAFARI": "sf",
		"ANDROID": "an"
	};

	var ua = navigator.userAgent;

	/*!
	 * Taken from jQuery JavaScript Library v1.7.1
	 * http://jquery.com/
	 *
	 * Copyright 2011, John Resig
	 * Dual licensed under the MIT or GPL Version 2 licenses.
	 * http://jquery.org/license
	 *
	 * Includes Sizzle.js
	 * http://sizzlejs.com/
	 * Copyright 2011, The Dojo Foundation
	 * Released under the MIT, BSD, and GPL Licenses.
	 *
	 * Date: Mon Nov 21 21:11:03 2011 -0500
	 */
	function calcBrowser(customUa){
		var _ua = (customUa || ua).toLowerCase(); // use custom user-agent if given

		var rwebkit = /(webkit)[ \/]([\w.]+)/;
		var ropera = /(opera)(?:.*version)?[ \/]([\w.]+)/;
		var rmsie = /(msie) ([\w.]+)/;
		var rmsie11 = /(trident)\/[\w.]+;.*rv:([\w.]+)/;
		var redge = /(edge)[ \/]([\w.]+)/;
		var rmozilla = /(mozilla)(?:.*? rv:([\w.]+))?/;

		// WinPhone IE11 and MS Edge userAgents contain "WebKit" and "Mozilla" and therefore must be checked first
		var browserMatch = redge.exec( _ua ) ||
					rmsie11.exec( _ua ) ||
					rwebkit.exec( _ua ) ||
					ropera.exec( _ua ) ||
					rmsie.exec( _ua ) ||
					_ua.indexOf("compatible") < 0 && rmozilla.exec( _ua ) ||
					[];

		var res = { browser: browserMatch[1] || "", version: browserMatch[2] || "0" };
		res[res.browser] = true;
		return res;
	}

	function getBrowser(customUa, customNav) {
		var b = calcBrowser(customUa);
		var _ua = customUa || ua;
		var _navigator = customNav || window.navigator;

		// jQuery checks for user agent strings. We differentiate between browsers
		var oExpMobile;
		if ( b.mozilla ) {
			oExpMobile = /Mobile/;
			if ( _ua.match(/Firefox\/(\d+\.\d+)/) ) {
				var version = parseFloat(RegExp.$1);
				return {
					name: BROWSER.FIREFOX,
					versionStr: "" + version,
					version: version,
					mozilla: true,
					mobile: oExpMobile.test(_ua)
				};
			} else {
				// unknown mozilla browser
				return {
					mobile: oExpMobile.test(_ua),
					mozilla: true,
					version: -1
				};
			}
		} else if ( b.webkit ) {
			// webkit version is needed for calculation if the mobile android device is a tablet (calculation of other mobile devices work without)
			var regExpWebkitVersion = _ua.toLowerCase().match(/webkit[\/]([\d.]+)/);
			var webkitVersion;
			if (regExpWebkitVersion) {
				webkitVersion = regExpWebkitVersion[1];
			}
			oExpMobile = /Mobile/;
			if ( _ua.match(/(Chrome|CriOS)\/(\d+\.\d+).\d+/)) {
				var version = parseFloat(RegExp.$2);
				return {
					name: BROWSER.CHROME,
					versionStr: "" + version,
					version: version,
					mobile: oExpMobile.test(_ua),
					webkit: true,
					webkitVersion: webkitVersion
				};
			} else if ( _ua.match(/FxiOS\/(\d+\.\d+)/)) {
				var version = parseFloat(RegExp.$1);
				return {
					name: BROWSER.FIREFOX,
					versionStr: "" + version,
					version: version,
					mobile: true,
					webkit: true,
					webkitVersion: webkitVersion
				};
			} else if ( _ua.match(/Android .+ Version\/(\d+\.\d+)/) ) {
				var version = parseFloat(RegExp.$1);
				return {
					name: BROWSER.ANDROID,
					versionStr: "" + version,
					version: version,
					mobile: oExpMobile.test(_ua),
					webkit: true,
					webkitVersion: webkitVersion
				};
			} else { // Safari might have an issue with _ua.match(...); thus changing
				var oExp = /(Version|PhantomJS)\/(\d+\.\d+).*Safari/;
				var bStandalone = _navigator.standalone;
				if (oExp.test(_ua)) {
					var aParts = oExp.exec(_ua);
					var version = parseFloat(aParts[2]);
					return {
						name: BROWSER.SAFARI,
						versionStr: "" + version,
						fullscreen: false,
						webview: false,
						version: version,
						mobile: oExpMobile.test(_ua),
						webkit: true,
						webkitVersion: webkitVersion,
						phantomJS: aParts[1] === "PhantomJS"
					};
				} else if (/iPhone|iPad|iPod/.test(_ua) && !(/CriOS/.test(_ua)) && !(/FxiOS/.test(_ua)) && (bStandalone === true || bStandalone === false)) {
					//WebView or Standalone mode on iOS
					return {
						name: BROWSER.SAFARI,
						version: -1,
						fullscreen: bStandalone,
						webview: !bStandalone,
						mobile: oExpMobile.test(_ua),
						webkit: true,
						webkitVersion: webkitVersion
					};
				} else { // other webkit based browser
					return {
						mobile: oExpMobile.test(_ua),
						webkit: true,
						webkitVersion: webkitVersion,
						version: -1
					};
				}
			}
		} else if ( b.msie || b.trident ) {
			var version;
			// recognize IE8 when running in compat mode (only then the documentMode property is there)
			if (document.documentMode && !customUa) { // only use the actual documentMode when no custom user-agent was given
				if (document.documentMode === 7) { // OK, obviously we are IE and seem to be 7... but as documentMode is there this cannot be IE7!
					version = 8.0;
				} else {
					version = parseFloat(document.documentMode);
				}
			} else {
				version = parseFloat(b.version);
			}
			return {
				name: BROWSER.INTERNET_EXPLORER,
				versionStr: "" + version,
				version: version,
				msie: true,
				mobile: false // TODO: really?
			};
		} else if ( b.edge ) {
			var version = version = parseFloat(b.version);
			return {
				name: BROWSER.EDGE,
				versionStr: "" + version,
				version: version,
				edge: true
			};
		}
		return {
			name: "",
			versionStr: "",
			version: -1,
			mobile: false
		};
	}
	device._testUserAgent = getBrowser; // expose the user-agent parsing (mainly for testing), but don't let it be overwritten

	function setBrowser() {
		device.browser = getBrowser();
		device.browser.BROWSER = BROWSER;

		if (device.browser.name) {
			for (var b in BROWSER) {
				if (BROWSER[b] === device.browser.name) {
					device.browser[b.toLowerCase()] = true;
				}
			}
		}
	}
	setBrowser();




//******** Support Detection ********

	/**
	 * Contains information about detected capabilities of the used browser or device.
	 *
	 * @namespace
	 * @name sap.ui.Device.support
	 * @public
	 */

	/**
	 * If this flag is set to <code>true</code>, the used browser supports touch events.
	 *
	 * <b>Note:</b> This flag indicates whether the used browser supports touch events or not.
	 * This does not necessarily mean that the used device has a touchable screen.
	 *
	 * @name sap.ui.Device.support.touch
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the used browser supports pointer events.
	 *
	 * @name sap.ui.Device.support.pointer
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the used browser natively supports media queries via JavaScript.
	 *
	 * <b>Note:</b> The {@link sap.ui.Device.media media queries API} of the device API can also be used when there is no native support.
	 *
	 * @name sap.ui.Device.support.matchmedia
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the used browser natively supports events of media queries via JavaScript.
	 *
	 * <b>Note:</b> The {@link sap.ui.Device.media media queries API} of the device API can also be used when there is no native support.
	 *
	 * @name sap.ui.Device.support.matchmedialistener
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the used browser natively supports the <code>orientationchange</code> event.
	 *
	 * <b>Note:</b> The {@link sap.ui.Device.orientation orientation event} of the device API can also be used when there is no native support.
	 *
	 * @name sap.ui.Device.support.orientation
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the device has a display with a high resolution.
	 *
	 * @name sap.ui.Device.support.retina
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the used browser supports web sockets.
	 *
	 * @name sap.ui.Device.support.websocket
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the used browser supports the <code>placeholder</code> attribute on <code>input</code> elements.
	 *
	 * @name sap.ui.Device.support.input.placeholder
	 * @type boolean
	 * @public
	 */

	device.support = {};

	//Maybe better to but this on device.browser because there are cases that a browser can touch but a device can't!
	device.support.touch = !!(('ontouchstart' in window) || window.DocumentTouch && document instanceof window.DocumentTouch);

	// FIXME: PhantomJS doesn't support touch events but exposes itself as touch
	//        enabled browser. Therfore we manually override that in jQuery.support!
	//        This has been tested with PhantomJS 1.9.7 and 2.0.0!
	if (device.browser.phantomJS) {
		device.support.touch = false;
	}

	device.support.pointer = !!window.PointerEvent;

	device.support.matchmedia = !!window.matchMedia;
	var m = device.support.matchmedia ? window.matchMedia("all and (max-width:0px)") : null; //IE10 doesn't like empty string as argument for matchMedia, FF returns null when running within an iframe with display:none
	device.support.matchmedialistener = !!(m && m.addListener);
	if (device.browser.safari && device.browser.version < 6 && !device.browser.fullscreen && !device.browser.webview) {
		//Safari seems to have addListener but no events are fired ?!
		device.support.matchmedialistener = false;
	}

	device.support.orientation = !!("orientation" in window && "onorientationchange" in window);

	device.support.retina = (window.retina || window.devicePixelRatio >= 2);

	device.support.websocket = ('WebSocket' in window);

	device.support.input = {};
	device.support.input.placeholder = ('placeholder' in document.createElement("input"));

//******** Match Media ********

	/**
	 * Event API for screen width changes.
	 *
	 * This API is based on media queries but can also be used if media queries are not natively supported by the used browser.
	 * In this case, the behavior of media queries is simulated by this API.
	 *
	 * There are several predefined {@link sap.ui.Device.media.RANGESETS range sets} available. Each of them defines a
	 * set of intervals for the screen width (from small to large). Whenever the screen width changes and the current screen width is in
	 * a different interval to the one before the change, the registered event handlers for the range set are called.
	 *
	 * If needed, it is also possible to define a custom set of intervals.
	 *
	 * The following example shows a typical use case:
	 * <pre>
	 * function sizeChanged(mParams) {
	 *     switch(mParams.name) {
	 *         case "Phone":
	 *             // Do what is needed for a little screen
	 *             break;
	 *         case "Tablet":
	 *             // Do what is needed for a medium sized screen
	 *             break;
	 *         case "Desktop":
	 *             // Do what is needed for a large screen
	 *     }
	 * }
	 *
	 * // Register an event handler to changes of the screen size
	 * sap.ui.Device.media.attachHandler(sizeChanged, null, sap.ui.Device.media.RANGESETS.SAP_STANDARD);
	 * // Do some initialization work based on the current size
	 * sizeChanged(sap.ui.Device.media.getCurrentRange(sap.ui.Device.media.RANGESETS.SAP_STANDARD));
	 * </pre>
	 *
	 * @namespace
	 * @name sap.ui.Device.media
	 * @public
	 */
	device.media = {};

	/**
	 * Enumeration containing the names and settings of predefined screen width media query range sets.
	 *
	 * @namespace
	 * @name sap.ui.Device.media.RANGESETS
	 * @public
	 */

	/**
	 * A 3-step range set (S-L).
	 *
	 * The ranges of this set are:
	 * <ul>
	 * <li><code>"S"</code>: For screens smaller than 520 pixels.</li>
	 * <li><code>"M"</code>: For screens greater than or equal to 520 pixels and smaller than 960 pixels.</li>
	 * <li><code>"L"</code>: For screens greater than or equal to 960 pixels.</li>
	 * </ul>
	 *
	 * To use this range set, you must initialize it explicitly ({@link sap.ui.Device.media.initRangeSet}).
	 *
	 * If this range set is initialized, a CSS class is added to the page root (<code>html</code> tag) which indicates the current
	 * screen width range: <code>sapUiMedia-3Step-<i>NAME_OF_THE_INTERVAL</i></code>.
	 *
	 * @name sap.ui.Device.media.RANGESETS.SAP_3STEPS
	 * @public
	 */
	/**
	 * A 4-step range set (S-XL).
	 *
	 * The ranges of this set are:
	 * <ul>
	 * <li><code>"S"</code>: For screens smaller than 520 pixels.</li>
	 * <li><code>"M"</code>: For screens greater than or equal to 520 pixels and smaller than 760 pixels.</li>
	 * <li><code>"L"</code>: For screens greater than or equal to 760 pixels and smaller than 960 pixels.</li>
	 * <li><code>"XL"</code>: For screens greater than or equal to 960 pixels.</li>
	 * </ul>
	 *
	 * To use this range set, you must initialize it explicitly ({@link sap.ui.Device.media.initRangeSet}).
	 *
	 * If this range set is initialized, a CSS class is added to the page root (<code>html</code> tag) which indicates the current
	 * screen width range: <code>sapUiMedia-4Step-<i>NAME_OF_THE_INTERVAL</i></code>.
	 *
	 * @name sap.ui.Device.media.RANGESETS.SAP_4STEPS
	 * @public
	 */
	/**
	 * A 6-step range set (XS-XXL).
	 *
	 * The ranges of this set are:
	 * <ul>
	 * <li><code>"XS"</code>: For screens smaller than 241 pixels.</li>
	 * <li><code>"S"</code>: For screens greater than or equal to 241 pixels and smaller than 400 pixels.</li>
	 * <li><code>"M"</code>: For screens greater than or equal to 400 pixels and smaller than 541 pixels.</li>
	 * <li><code>"L"</code>: For screens greater than or equal to 541 pixels and smaller than 768 pixels.</li>
	 * <li><code>"XL"</code>: For screens greater than or equal to 768 pixels and smaller than 960 pixels.</li>
	 * <li><code>"XXL"</code>: For screens greater than or equal to 960 pixels.</li>
	 * </ul>
	 *
	 * To use this range set, you must initialize it explicitly ({@link sap.ui.Device.media.initRangeSet}).
	 *
	 * If this range set is initialized, a CSS class is added to the page root (<code>html</code> tag) which indicates the current
	 * screen width range: <code>sapUiMedia-6Step-<i>NAME_OF_THE_INTERVAL</i></code>.
	 *
	 * @name sap.ui.Device.media.RANGESETS.SAP_6STEPS
	 * @public
	 */
	/**
	 * A 3-step range set (Phone, Tablet, Desktop).
	 *
	 * The ranges of this set are:
	 * <ul>
	 * <li><code>"Phone"</code>: For screens smaller than 600 pixels.</li>
	 * <li><code>"Tablet"</code>: For screens greater than or equal to 600 pixels and smaller than 1024 pixels.</li>
	 * <li><code>"Desktop"</code>: For screens greater than or equal to 1024 pixels.</li>
	 * </ul>
	 *
	 * This range set is initialized by default. An initialization via {@link sap.ui.Device.media.initRangeSet} is not needed.
	 *
	 * A CSS class is added to the page root (<code>html</code> tag) which indicates the current
	 * screen width range: <code>sapUiMedia-Std-<i>NAME_OF_THE_INTERVAL</i></code>.
	 * Furthermore there are 5 additional CSS classes to hide elements based on the width of the screen:
	 * <ul>
	 * <li><code>sapUiHideOnPhone</code>: Will be hidden if the screen has 600px or more</li>
	 * <li><code>sapUiHideOnTablet</code>: Will be hidden if the screen has less than 600px or more than 1023px</li>
	 * <li><code>sapUiHideOnDesktop</code>: Will be hidden if the screen is smaller than 1024px</li>
	 * <li><code>sapUiVisibleOnlyOnPhone</code>: Will be visible if the screen has less than 600px</li>
	 * <li><code>sapUiVisibleOnlyOnTablet</code>: Will be visible if the screen has 600px or more but less than 1024px</li>
	 * <li><code>sapUiVisibleOnlyOnDesktop</code>: Will be visible if the screen has 1024px or more</li>
	 * </ul>
	 *
	 * @name sap.ui.Device.media.RANGESETS.SAP_STANDARD
	 * @public
	 */

	/**
	 * A 4-step range set (Phone, Tablet, Desktop, LargeDesktop).
	 *
	 * The ranges of this set are:
	 * <ul>
	 * <li><code>"Phone"</code>: For screens smaller than 600 pixels.</li>
	 * <li><code>"Tablet"</code>: For screens greater than or equal to 600 pixels and smaller than 1024 pixels.</li>
	 * <li><code>"Desktop"</code>: For screens greater than or equal to 1024 pixels and smaller than 1440 pixels.</li>
	 * <li><code>"LargeDesktop"</code>: For screens greater than or equal to 1440 pixels.</li>
	 * </ul>
	 *
	 * This range set is initialized by default. An initialization via {@link sap.ui.Device.media.initRangeSet} is not needed.
	 *
	 * A CSS class is added to the page root (<code>html</code> tag) which indicates the current
	 * screen width range: <code>sapUiMedia-StdExt-<i>NAME_OF_THE_INTERVAL</i></code>.
	 *
	 * @name sap.ui.Device.media.RANGESETS.SAP_STANDARD_EXTENDED
	 * @public
	 */

	var RANGESETS = {
		"SAP_3STEPS": "3Step",
		"SAP_4STEPS": "4Step",
		"SAP_6STEPS": "6Step",
		"SAP_STANDARD": "Std",
		"SAP_STANDARD_EXTENDED": "StdExt"
	};
	device.media.RANGESETS = RANGESETS;
	device.media._predefinedRangeSets = {};
	device.media._predefinedRangeSets[RANGESETS.SAP_3STEPS] = {points: [520, 960], unit: "px", name: RANGESETS.SAP_3STEPS, names: ["S", "M", "L"]};
	device.media._predefinedRangeSets[RANGESETS.SAP_4STEPS] = {points: [520, 760, 960], unit: "px", name: RANGESETS.SAP_4STEPS, names: ["S", "M", "L", "XL"]};
	device.media._predefinedRangeSets[RANGESETS.SAP_6STEPS] = {points: [241, 400, 541, 768, 960], unit: "px", name: RANGESETS.SAP_6STEPS, names: ["XS", "S", "M", "L", "XL", "XXL"]};
	device.media._predefinedRangeSets[RANGESETS.SAP_STANDARD] = {points: [600, 1024], unit: "px", name: RANGESETS.SAP_STANDARD, names: ["Phone", "Tablet", "Desktop"]};
	device.media._predefinedRangeSets[RANGESETS.SAP_STANDARD_EXTENDED] = {points: [600, 1024, 1440], unit: "px", name: RANGESETS.SAP_STANDARD_EXTENDED, names: ["Phone", "Tablet", "Desktop", "LargeDesktop"]};
	var _defaultRangeSet = RANGESETS.SAP_STANDARD;
	var media_timeout = device.support.matchmedialistener ? 0 : 100;
	var _querysets = {};
	var media_currentwidth = null;

	function getQuery(from, to, unit){
		unit = unit || "px";
		var q = "all";
		if (from > 0) {
			q = q + " and (min-width:" + from + unit + ")";
		}
		if (to > 0) {
			q = q + " and (max-width:" + to + unit + ")";
		}
		return q;
	}

	function handleChange(name){
		if (!device.support.matchmedialistener && media_currentwidth == windowSize()[0]) {
			return; //Skip unnecessary resize events
		}

		if (_querysets[name].timer) {
			clearTimeout(_querysets[name].timer);
			_querysets[name].timer = null;
		}

		_querysets[name].timer = setTimeout(function() {
			var mParams = checkQueries(name, false);
			if (mParams) {
				fireEvent("media_" + name, mParams);
			}
		}, media_timeout);
	}

	function getRangeInfo(sSetName, iRangeIdx){
		var q = _querysets[sSetName].queries[iRangeIdx];
		var info = {from: q.from, unit: _querysets[sSetName].unit};
		if (q.to >= 0) {
			info.to = q.to;
		}
		if (_querysets[sSetName].names) {
			info.name = _querysets[sSetName].names[iRangeIdx];
		}
		return info;
	}

	function checkQueries(name, infoOnly, fnMatches){
		fnMatches = fnMatches || device.media.matches;
		if (_querysets[name]) {
			var aQueries = _querysets[name].queries;
			var info = null;
			for (var i = 0, len = aQueries.length; i < len; i++) {
				var q = aQueries[i];
				if ((q != _querysets[name].currentquery || infoOnly) && fnMatches(q.from, q.to, _querysets[name].unit)) {
					if (!infoOnly) {
						_querysets[name].currentquery = q;
					}
					if (!_querysets[name].noClasses && _querysets[name].names && !infoOnly) {
						refreshCSSClasses(name, _querysets[name].names[i]);
					}
					info = getRangeInfo(name, i);
				}
			}

			return info;
		}
		logger.log(WARNING, "No queryset with name " + name + " found", 'DEVICE.MEDIA');
		return null;
	}

	function refreshCSSClasses(sSetName, sRangeName, bRemove){
		 var sClassPrefix = "sapUiMedia-" + sSetName + "-";
		 changeRootCSSClass(sClassPrefix + sRangeName, bRemove, sClassPrefix);
	}

	function changeRootCSSClass(sClassName, bRemove, sPrefix){
		var oRoot = document.documentElement;
		if (oRoot.className.length == 0) {
			if (!bRemove) {
				oRoot.className = sClassName;
			}
		} else {
			var aCurrentClasses = oRoot.className.split(" ");
			var sNewClasses = "";
			for (var i = 0; i < aCurrentClasses.length; i++) {
				if ((sPrefix && aCurrentClasses[i].indexOf(sPrefix) != 0) || (!sPrefix && aCurrentClasses[i] != sClassName)) {
					sNewClasses = sNewClasses + aCurrentClasses[i] + " ";
				}
			}
			if (!bRemove) {
				sNewClasses = sNewClasses + sClassName;
			}
			oRoot.className = sNewClasses;
		}
	}

	function windowSize(){

		return [window.innerWidth, window.innerHeight];
	}

	function convertToPx(val, unit){
		if (unit === "em" || unit === "rem") {
			var s = window.getComputedStyle || function(e) {
					return e.currentStyle;
				};
				var x = s(document.documentElement).fontSize;
				var f = (x && x.indexOf("px") >= 0) ? parseFloat(x, 10) : 16;
				return val * f;
		}
		return val;
	}

	function match_legacy_by_size (from, to, unit, size) {
		from = convertToPx(from, unit);
		to = convertToPx(to, unit);

		var width = size[0];
		var a = from < 0 || from <= width;
		var b = to < 0 || width <= to;
		return a && b;
	}

	function match_legacy(from, to, unit){
		return match_legacy_by_size(from, to, unit, windowSize());
	}

	function match(from, to, unit){
		var q = getQuery(from, to, unit);
		var mm = window.matchMedia(q); //FF returns null when running within an iframe with display:none
		return mm && mm.matches;
	}

	device.media.matches = device.support.matchmedia ? match : match_legacy;

	/**
	 * Registers the given event handler to change events of the screen width based on the range set with the specified name.
	 *
	 * The event is fired whenever the screen width changes and the current screen width is in
	 * a different interval of the given range set than before the width change.
	 *
	 * The event handler is called with a single argument: a map <code>mParams</code> which provides the following information
	 * about the entered interval:
	 * <ul>
	 * <li><code>mParams.from</code>: The start value (inclusive) of the entered interval as a number</li>
	 * <li><code>mParams.to</code>: The end value (exclusive) range of the entered interval as a number or undefined for the last interval (infinity)</li>
	 * <li><code>mParams.unit</code>: The unit used for the values above, e.g. <code>"px"</code></li>
	 * <li><code>mParams.name</code>: The name of the entered interval, if available</li>
	 * </ul>
	 *
	 * @param {function}
	 *            fnFunction The handler function to call when the event occurs. This function will be called in the context of the
	 *                       <code>oListener</code> instance (if present) or on the <code>window</code> instance. A map with information
	 *                       about the entered range set is provided as a single argument to the handler (see details above).
	 * @param {object}
	 *            [oListener] The object that wants to be notified when the event occurs (<code>this</code> context within the
	 *                        handler function). If it is not specified, the handler function is called in the context of the <code>window</code>.
	 * @param {string}
	 *            sName The name of the range set to listen to. The range set must be initialized beforehand
	 *                  ({@link sap.ui.Device.media.initRangeSet}). If no name is provided, the
	 *                  {@link sap.ui.Device.media.RANGESETS.SAP_STANDARD default range set} is used.
	 *
	 * @name sap.ui.Device.media.attachHandler
	 * @function
	 * @public
	 */
	device.media.attachHandler = function(fnFunction, oListener, sName){
		var name = sName || _defaultRangeSet;
		attachEvent("media_" + name, fnFunction, oListener);
	};

	/**
	 * Removes a previously attached event handler from the change events of the screen width.
	 *
	 * The passed parameters must match those used for registration with {@link #.attachHandler} beforehand.
	 *
	 * @param {function}
	 *            fnFunction The handler function to detach from the event
	 * @param {object}
	 *            [oListener] The object that wanted to be notified when the event occurred
	 * @param {string}
	 *             sName The name of the range set to listen to. If no name is provided, the
	 *                   {@link sap.ui.Device.media.RANGESETS.SAP_STANDARD default range set} is used.
	 *
	 * @name sap.ui.Device.media.detachHandler
	 * @function
	 * @public
	 */
	device.media.detachHandler = function(fnFunction, oListener, sName){
		var name = sName || _defaultRangeSet;
		detachEvent("media_" + name, fnFunction, oListener);
	};

	/**
	 * Initializes a screen width media query range set.
	 *
	 * This initialization step makes the range set ready to be used for one of the other functions in namespace <code>sap.ui.Device.media</code>.
	 * The most important {@link sap.ui.Device.media.RANGESETS predefined range sets} are initialized automatically.
	 *
	 * To make a not yet initialized {@link sap.ui.Device.media.RANGESETS predefined range set} ready to be used, call this function with the
	 * name of the range set to be initialized:
	 * <pre>
	 * sap.ui.Device.media.initRangeSet(sap.ui.Device.media.RANGESETS.SAP_3STEPS);
	 * </pre>
	 *
	 * Alternatively it is possible to define custom range sets as shown in the following example:
	 * <pre>
	 * sap.ui.Device.media.initRangeSet("MyRangeSet", [200, 400], "px", ["Small", "Medium", "Large"]);
	 * </pre>
	 * This example defines the following named ranges:
	 * <ul>
	 * <li><code>"Small"</code>: For screens smaller than 200 pixels.</li>
	 * <li><code>"Medium"</code>: For screens greater than or equal to 200 pixels and smaller than 400 pixels.</li>
	 * <li><code>"Large"</code>: For screens greater than or equal to 400 pixels.</li>
	 * </ul>
	 * The range names are optional. If they are specified a CSS class (e.g. <code>sapUiMedia-MyRangeSet-Small</code>) is also
	 * added to the document root depending on the current active range. This can be suppressed via parameter <code>bSuppressClasses</code>.
	 *
	 * @param {string}
	 *             sName The name of the range set to be initialized - either a {@link sap.ui.Device.media.RANGESETS predefined} or custom one.
	 *                   The name must be a valid id and consist only of letters and numeric digits.
	 * @param {int[]}
	 *             [aRangeBorders] The range borders
	 * @param {string}
	 *             [sUnit] The unit which should be used for the values given in <code>aRangeBorders</code>.
	 *                     The allowed values are <code>"px"</code> (default), <code>"em"</code> or <code>"rem"</code>
	 * @param {string[]}
	 *             [aRangeNames] The names of the ranges. The names must be a valid id and consist only of letters and digits. If names
	 *             are specified, CSS classes are also added to the document root as described above. This behavior can be
	 *             switched off explicitly by using <code>bSuppressClasses</code>. <b>Note:</b> <code>aRangeBorders</code> with <code>n</code> entries
	 *             define <code>n+1</code> ranges. Therefore <code>n+1</code> names must be provided.
	 * @param {boolean}
	 *             [bSuppressClasses] Whether or not writing of CSS classes to the document root should be suppressed when
	 *             <code>aRangeNames</code> are provided
	 *
	 * @name sap.ui.Device.media.initRangeSet
	 * @function
	 * @public
	 */
	device.media.initRangeSet = function(sName, aRangeBorders, sUnit, aRangeNames, bSuppressClasses){
		//TODO Do some Assertions and parameter checking
		var oConfig;
		if (!sName) {
			oConfig = device.media._predefinedRangeSets[_defaultRangeSet];
		} else if (sName && device.media._predefinedRangeSets[sName]) {
			oConfig = device.media._predefinedRangeSets[sName];
		} else {
			oConfig = {name: sName, unit: (sUnit || "px").toLowerCase(), points: aRangeBorders || [], names: aRangeNames, noClasses: !!bSuppressClasses};
		}

		if (device.media.hasRangeSet(oConfig.name)) {
			logger.log(INFO, "Range set " + oConfig.name + " has already been initialized", 'DEVICE.MEDIA');
			return;
		}

		sName = oConfig.name;
		oConfig.queries = [];
		oConfig.timer = null;
		oConfig.currentquery = null;
		oConfig.listener = function(){
			return handleChange(sName);
		};

		var from, to, query;
		var aPoints = oConfig.points;
		for (var i = 0, len = aPoints.length; i <= len; i++) {
			from = (i == 0) ? 0 : aPoints[i - 1];
			to = (i == aPoints.length) ? -1 : aPoints[i];
			query = getQuery(from, to, oConfig.unit);
			oConfig.queries.push({
				query: query,
				from: from,
				to: to
			});
		}

		if (oConfig.names && oConfig.names.length != oConfig.queries.length) {
			oConfig.names = null;
		}

		_querysets[oConfig.name] = oConfig;

		if (device.support.matchmedialistener) { //FF, Safari, Chrome, IE10?
			var queries = oConfig.queries;
			for (var i = 0; i < queries.length; i++) {
				var q = queries[i];
				q.media = window.matchMedia(q.query);
				q.media.addListener(oConfig.listener);
			}
		} else { //IE, Safari (<6?)
			if (window.addEventListener) {
				window.addEventListener("resize", oConfig.listener, false);
				window.addEventListener("orientationchange", oConfig.listener, false);
			} else { //IE8
				window.attachEvent("onresize", oConfig.listener);
			}
		}

		oConfig.listener();
	};

	/**
	 * Returns information about the current active range of the range set with the given name.
	 *
	 * If the optional parameter <code>iWidth</iWidth> is given, the active range will be determined for that width,
	 * otherwise it is determined for the current window size.
	 *
	 * @param {string} sName The name of the range set. The range set must be initialized beforehand ({@link sap.ui.Device.media.initRangeSet})
	 * @param {int} [iWidth] An optional width, based on which the range should be determined;
	 *             If <code>iWidth</code> is not a number, the window size will be used.
	 * @returns {map} Information about the current active interval of the range set. The returned map has the same structure as the argument of the event handlers ({@link sap.ui.Device.media.attachHandler})
	 *
	 * @name sap.ui.Device.media.getCurrentRange
	 * @function
	 * @public
	 */
	device.media.getCurrentRange = function(sName, iWidth){
		if (!device.media.hasRangeSet(sName)) {
			return null;
		}
		return checkQueries(sName, true, isNaN(iWidth) ? null : function(from, to, unit) {
			return match_legacy_by_size(from, to, unit, [iWidth, 0]);
		});
	};

	/**
	 * Returns <code>true</code> if a range set with the given name is already initialized.
	 *
	 * @param {string} sName The name of the range set.
	 *
	 * @name sap.ui.Device.media.hasRangeSet
	 * @return {boolean} Returns <code>true</code> if a range set with the given name is already initialized
	 * @function
	 * @public
	 */
	device.media.hasRangeSet = function(sName){
		return sName && !!_querysets[sName];
	};

	/**
	 * Removes a previously initialized range set and detaches all registered handlers.
	 *
	 * Only custom range sets can be removed via this function. Initialized predefined range sets
	 * ({@link sap.ui.Device.media.RANGESETS}) cannot be removed.
	 *
	 * @param {string} sName The name of the range set which should be removed.
	 *
	 * @name sap.ui.Device.media.removeRangeSet
	 * @function
	 * @protected
	 */
	device.media.removeRangeSet = function(sName){
		if (!device.media.hasRangeSet(sName)) {
			logger.log(INFO, "RangeSet " + sName + " not found, thus could not be removed.", 'DEVICE.MEDIA');
			return;
		}

		for (var x in RANGESETS) {
			if (sName === RANGESETS[x]) {
				logger.log(WARNING, "Cannot remove default rangeset - no action taken.", 'DEVICE.MEDIA');
				return;
			}
		}

		var oConfig = _querysets[sName];
		if (device.support.matchmedialistener) { //FF, Safari, Chrome, IE10?
			var queries = oConfig.queries;
			for (var i = 0; i < queries.length; i++) {
				queries[i].media.removeListener(oConfig.listener);
			}
		} else { //IE, Safari (<6?)
			if (window.removeEventListener) {
				window.removeEventListener("resize", oConfig.listener, false);
				window.removeEventListener("orientationchange", oConfig.listener, false);
			} else { //IE8
				window.detachEvent("onresize", oConfig.listener);
			}
		}

		refreshCSSClasses(sName, "", true);
		delete mEventRegistry["media_" + sName];
		delete _querysets[sName];
	};

//******** System Detection ********

	/**
	 * Provides a basic categorization of the used device based on various indicators.
	 *
	 * These indicators are for example the support of touch events, the screen size, the used operation system or
	 * the user agent of the browser.
	 *
	 * <b>Note:</b> Depending on the capabilities of the device it is also possible that multiple flags are set to <code>true</code>.
	 *
	 * @namespace
	 * @name sap.ui.Device.system
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the device is recognized as a tablet.
	 *
	 * Furthermore, a CSS class <code>sap-tablet</code> is added to the document root element.
	 *
	 * <b>Note:</b> This flag is also true for some browsers on desktop devices running on Windows 8 or higher. Also see the
	 * documentation for {@link sap.ui.Device.system.combi} devices.
	 * You can use the following logic to ensure that the current device is a tablet device:
	 *
	 * <pre>
	 * if(sap.ui.Device.system.tablet && !sap.ui.Device.system.desktop){
	 *	...tablet related commands...
	 * }
	 * </pre>
	 *
	 * @name sap.ui.Device.system.tablet
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the device is recognized as a phone.
	 *
	 * Furthermore, a CSS class <code>sap-phone</code> is added to the document root element.
	 *
	 * @name sap.ui.Device.system.phone
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the device is recognized as a desktop system.
	 *
	 * Furthermore, a CSS class <code>sap-desktop</code> is added to the document root element.
	 *
	 * @name sap.ui.Device.system.desktop
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the device is recognized as a combination of a desktop system and tablet.
	 *
	 * Furthermore, a CSS class <code>sap-combi</code> is added to the document root element.
	 *
	 * <b>Note:</b> This property is mainly for Microsoft Windows 8 (and following) devices where the mouse and touch event may be supported
	 * natively by the browser being used. This property is set to <code>true</code> only when both mouse and touch event are natively supported.
	 *
	 * @name sap.ui.Device.system.combi
	 * @type boolean
	 * @public
	 */
	/**
	 * Enumeration containing the names of known types of the devices.
	 *
	 * @namespace
	 * @name sap.ui.Device.system.SYSTEMTYPE
	 * @private
	 */

	var SYSTEMTYPE = {
			"TABLET" : "tablet",
			"PHONE" : "phone",
			"DESKTOP" : "desktop",
			"COMBI" : "combi"
	};

	device.system = {};

	function getSystem(_simMobileOnDesktop, customUA) {
		var t = isTablet(customUA);
		var isWin8Upwards = device.os.windows && device.os.version >= 8;
		var isWin7 = device.os.windows && device.os.version === 7;

		var s = {};
		s.tablet = !!(((device.support.touch && !isWin7) || isWin8Upwards || !!_simMobileOnDesktop) && t);
		s.phone = !!(device.os.windows_phone || ((device.support.touch && !isWin7) || !!_simMobileOnDesktop) && !t);
		s.desktop = !!((!s.tablet && !s.phone) || isWin8Upwards || isWin7);
		s.combi = !!(s.desktop && s.tablet);
		s.SYSTEMTYPE = SYSTEMTYPE;

		for (var type in SYSTEMTYPE) {
			changeRootCSSClass("sap-" + SYSTEMTYPE[type], !s[SYSTEMTYPE[type]]);
		}
		return s;
	}

	function isTablet(customUA) {
		var ua = customUA || navigator.userAgent;
		var isWin8Upwards = device.os.windows && device.os.version >= 8;
		if (device.os.name === device.os.OS.IOS) {
			return /ipad/i.test(ua);
		} else {
			//in real mobile device
			if (device.support.touch) {
				if (isWin8Upwards) {
					return true;
				}

				if (device.browser.chrome && device.os.android && device.os.version >= 4.4) {
					// From Android version 4.4, WebView also uses Chrome as Kernel.
					// We can use the user agent pattern defined in Chrome to do phone/tablet detection
					// According to the information here: https://developer.chrome.com/multidevice/user-agent#chrome_for_android_user_agent,
					//  the existence of "Mobile" indicates it's a phone. But because the crosswalk framework which is used in Fiori Client
					//  inserts another "Mobile" to the user agent for both tablet and phone, we need to check whether "Mobile Safari/<Webkit Rev>" exists.
					return !/Mobile Safari\/[.0-9]+/.test(ua);
				} else {
					var densityFactor = window.devicePixelRatio ? window.devicePixelRatio : 1; // may be undefined in Windows Phone devices
					// On Android sometimes window.screen.width returns the logical CSS pixels, sometimes the physical device pixels;
					// Tests on multiple devices suggest this depends on the Webkit version.
					// The Webkit patch which changed the behavior was done here: https://bugs.webkit.org/show_bug.cgi?id=106460
					// Chrome 27 with Webkit 537.36 returns the logical pixels,
					// Chrome 18 with Webkit 535.19 returns the physical pixels.
					// The BlackBerry 10 browser with Webkit 537.10+ returns the physical pixels.
					// So it appears like somewhere above Webkit 537.10 we do not hve to divide by the devicePixelRatio anymore.
					if (device.os.android && device.browser.webkit && (parseFloat(device.browser.webkitVersion) > 537.10)) {
						densityFactor = 1;
					}

					//this is how android distinguishes between tablet and phone
					//http://android-developers.blogspot.de/2011/07/new-tools-for-managing-screen-sizes.html
					var bTablet = (Math.min(window.screen.width / densityFactor, window.screen.height / densityFactor) >= 600);

					// special workaround for Nexus 7 where the window.screen.width is 600px or 601px in portrait mode (=> tablet)
					// but window.screen.height 552px in landscape mode (=> phone), because the browser UI takes some space on top.
					// So the detected device type depends on the orientation :-(
					// actually this is a Chrome bug, as "width"/"height" should return the entire screen's dimensions and
					// "availWidth"/"availHeight" should return the size available after subtracting the browser UI
					if (isLandscape()
							&& (window.screen.height === 552 || window.screen.height === 553) // old/new Nexus 7
							&& (/Nexus 7/i.test(ua))) {
						bTablet = true;
					}

					return bTablet;
				}

			} else {
				// This simple android phone detection can be used here because this is the mobile emulation mode in desktop browser
				var android_phone = (/(?=android)(?=.*mobile)/i.test(ua));
				// in desktop browser, it's detected as tablet when
				// 1. Windows 8 device with a touch screen where "Touch" is contained in the userAgent
				// 2. Android emulation and it's not an Android phone
				return (device.browser.msie && ua.indexOf("Touch") !== -1) || (device.os.android && !android_phone);
			}
		}
	}

	function setSystem(_simMobileOnDesktop, customUA) {
		device.system = getSystem(_simMobileOnDesktop, customUA);
		if (device.system.tablet || device.system.phone) {
			device.browser.mobile = true;
		}
	}
	setSystem();
	// expose the function for unit test
	device._getSystem = getSystem;

//******** Orientation Detection ********

	/**
	 * Common API for orientation change notifications across all platforms.
	 *
	 * For browsers or devices that do not provide native support for orientation change events
	 * the API simulates them based on the ratio of the document's width and height.
	 *
	 * @namespace
	 * @name sap.ui.Device.orientation
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the screen is currently in portrait mode (the height is greater than the width).
	 *
	 * @name sap.ui.Device.orientation.portrait
	 * @type boolean
	 * @public
	 */
	/**
	 * If this flag is set to <code>true</code>, the screen is currently in landscape mode (the width is greater than the height).
	 *
	 * @name sap.ui.Device.orientation.landscape
	 * @type boolean
	 * @public
	 */

	device.orientation = {};

	/**
	 * Common API for document window size change notifications across all platforms.
	 *
	 * @namespace
	 * @name sap.ui.Device.resize
	 * @public
	 */
	/**
	 * The current height of the document's window in pixels.
	 *
	 * @name sap.ui.Device.resize.height
	 * @type integer
	 * @public
	 */
	/**
	 * The current width of the document's window in pixels.
	 *
	 * @name sap.ui.Device.resize.width
	 * @type integer
	 * @public
	 */

	device.resize = {};

	/**
	 * Registers the given event handler to orientation change events of the document's window.
	 *
	 * The event is fired whenever the screen orientation changes and the width of the document's window
	 * becomes greater than its height or the other way round.
	 *
	 * The event handler is called with a single argument: a map <code>mParams</code> which provides the following information:
	 * <ul>
	 * <li><code>mParams.landscape</code>: If this flag is set to <code>true</code>, the screen is currently in landscape mode, otherwise in portrait mode.</li>
	 * </ul>
	 *
	 * @param {function}
	 *            fnFunction The handler function to call when the event occurs. This function will be called in the context of the
	 *                       <code>oListener</code> instance (if present) or on the <code>window</code> instance. A map with information
	 *                       about the orientation is provided as a single argument to the handler (see details above).
	 * @param {object}
	 *            [oListener] The object that wants to be notified when the event occurs (<code>this</code> context within the
	 *                        handler function). If it is not specified, the handler function is called in the context of the <code>window</code>.
	 *
	 * @name sap.ui.Device.orientation.attachHandler
	 * @function
	 * @public
	 */
	device.orientation.attachHandler = function(fnFunction, oListener){
		attachEvent("orientation", fnFunction, oListener);
	};

	/**
	 * Registers the given event handler to resize change events of the document's window.
	 *
	 * The event is fired whenever the document's window size changes.
	 *
	 * The event handler is called with a single argument: a map <code>mParams</code> which provides the following information:
	 * <ul>
	 * <li><code>mParams.height</code>: The height of the document's window in pixels.</li>
	 * <li><code>mParams.width</code>: The width of the document's window in pixels.</li>
	 * </ul>
	 *
	 * @param {function}
	 *            fnFunction The handler function to call when the event occurs. This function will be called in the context of the
	 *                       <code>oListener</code> instance (if present) or on the <code>window</code> instance. A map with information
	 *                       about the size is provided as a single argument to the handler (see details above).
	 * @param {object}
	 *            [oListener] The object that wants to be notified when the event occurs (<code>this</code> context within the
	 *                        handler function). If it is not specified, the handler function is called in the context of the <code>window</code>.
	 *
	 * @name sap.ui.Device.resize.attachHandler
	 * @function
	 * @public
	 */
	device.resize.attachHandler = function(fnFunction, oListener){
		attachEvent("resize", fnFunction, oListener);
	};

	/**
	 * Removes a previously attached event handler from the orientation change events.
	 *
	 * The passed parameters must match those used for registration with {@link #.attachHandler} beforehand.
	 *
	 * @param {function}
	 *            fnFunction The handler function to detach from the event
	 * @param {object}
	 *            [oListener] The object that wanted to be notified when the event occurred
	 *
	 * @name sap.ui.Device.orientation.detachHandler
	 * @function
	 * @public
	 */
	device.orientation.detachHandler = function(fnFunction, oListener){
		detachEvent("orientation", fnFunction, oListener);
	};

	/**
	 * Removes a previously attached event handler from the resize events.
	 *
	 * The passed parameters must match those used for registration with {@link #.attachHandler} beforehand.
	 *
	 * @param {function}
	 *            fnFunction The handler function to detach from the event
	 * @param {object}
	 *            [oListener] The object that wanted to be notified when the event occurred
	 *
	 * @name sap.ui.Device.resize.detachHandler
	 * @function
	 * @public
	 */
	device.resize.detachHandler = function(fnFunction, oListener){
		detachEvent("resize", fnFunction, oListener);
	};

	function setOrientationInfo(oInfo){
		oInfo.landscape = isLandscape(true);
		oInfo.portrait = !oInfo.landscape;
	}

	function handleOrientationChange(){
		setOrientationInfo(device.orientation);
		fireEvent("orientation", {landscape: device.orientation.landscape});
	}

	function handleResizeChange(){
		setResizeInfo(device.resize);
		fireEvent("resize", {height: device.resize.height, width: device.resize.width});
	}

	function setResizeInfo(oInfo){
		oInfo.width = windowSize()[0];
		oInfo.height = windowSize()[1];
	}

	function handleOrientationResizeChange(){
		var wasL = device.orientation.landscape;
		var isL = isLandscape();
		if (wasL != isL) {
			handleOrientationChange();
		}
		//throttle resize events because most browsers throw one or more resize events per pixel
		//for every resize event inside the period from 150ms (starting from the first resize event),
		//we only fire one resize event after this period
		if (!iResizeTimeout) {
			iResizeTimeout = window.setTimeout(handleResizeTimeout, 150);
		}
	}

	function handleResizeTimeout() {
		handleResizeChange();
		iResizeTimeout = null;
	}

	var bOrientationchange = false;
	var bResize = false;
	var iOrientationTimeout;
	var iResizeTimeout;
	var iClearFlagTimeout;
	var iWindowHeightOld = windowSize()[1];
	var iWindowWidthOld = windowSize()[0];
	var bKeyboardOpen = false;
	var iLastResizeTime;
	var rInputTagRegex = /INPUT|TEXTAREA|SELECT/;
	// On iPhone with iOS version 7.0.x and on iPad with iOS version 7.x (tested with all versions below 7.1.1), there's a invalide resize event fired
	// when changing the orientation while keyboard is shown.
	var bSkipFirstResize = device.os.ios && device.browser.name === "sf" &&
		((device.system.phone && device.os.version >= 7 && device.os.version < 7.1) || (device.system.tablet && device.os.version >= 7));

	function isLandscape(bFromOrientationChange){
		if (device.support.touch && device.support.orientation && device.os.android) {
			//if on screen keyboard is open and the call of this method is from orientation change listener, reverse the last value.
			//this is because when keyboard opens on android device, the height can be less than the width even in portrait mode.
			if (bKeyboardOpen && bFromOrientationChange) {
				return !device.orientation.landscape;
			}
			if (bKeyboardOpen) { //when keyboard opens, the last orientation change value will be retured.
				return device.orientation.landscape;
			}
		} else if (device.support.matchmedia && device.support.orientation) { //most desktop browsers and windows phone/tablet which not support orientationchange
			return !!window.matchMedia("(orientation: landscape)").matches;
		}
		//otherwise compare the width and height of window
		var size = windowSize();
		return size[0] > size[1];
	}

	function handleMobileOrientationResizeChange(evt) {
		if (evt.type == "resize") {
			// supress the first invalid resize event fired before orientationchange event while keyboard is open on iPhone 7.0.x
			// because this event has wrong size infos
			if (bSkipFirstResize && rInputTagRegex.test(document.activeElement.tagName) && !bOrientationchange) {
				return;
			}

			var iWindowHeightNew = windowSize()[1];
			var iWindowWidthNew = windowSize()[0];
			var iTime = new Date().getTime();
			//skip multiple resize events by only one orientationchange
			if (iWindowHeightNew === iWindowHeightOld && iWindowWidthNew === iWindowWidthOld) {
				return;
			}
			bResize = true;
			//on mobile devices opening the keyboard on some devices leads to a resize event
			//in this case only the height changes, not the width
			if ((iWindowHeightOld != iWindowHeightNew) && (iWindowWidthOld == iWindowWidthNew)) {
				//Asus Transformer tablet fires two resize events when orientation changes while keyboard is open.
				//Between these two events, only the height changes. The check of if keyboard is open has to be skipped because
				//it may be judged as keyboard closed but the keyboard is still open which will affect the orientation detection
				if (!iLastResizeTime || (iTime - iLastResizeTime > 300)) {
					bKeyboardOpen = (iWindowHeightNew < iWindowHeightOld);
				}
				handleResizeChange();
			} else {
				iWindowWidthOld = iWindowWidthNew;
			}
			iLastResizeTime = iTime;
			iWindowHeightOld = iWindowHeightNew;

			if (iClearFlagTimeout) {
				window.clearTimeout(iClearFlagTimeout);
				iClearFlagTimeout = null;
			}
			//Some Android build-in browser fires a resize event after the viewport is applied.
			//This resize event has to be dismissed otherwise when the next orientationchange event happens,
			//a UI5 resize event will be fired with the wrong window size.
			iClearFlagTimeout = window.setTimeout(clearFlags, 1200);
		} else if (evt.type == "orientationchange") {
			bOrientationchange = true;
		}

		if (iOrientationTimeout) {
			clearTimeout(iOrientationTimeout);
			iOrientationTimeout = null;
		}
		iOrientationTimeout = window.setTimeout(handleMobileTimeout, 50);
	}

	function handleMobileTimeout() {
		// with ios split view, the browser fires only resize event and no orientationchange when changing the size of a split view
		// therefore the following if needs to be adapted with additional check of iPad with version greater or equal 9 (splitview was introduced with iOS 9)
		if (bResize && (bOrientationchange || (device.system.tablet && device.os.ios && device.os.version >= 9))) {
			handleOrientationChange();
			handleResizeChange();
			bOrientationchange = false;
			bResize = false;
			if (iClearFlagTimeout) {
				window.clearTimeout(iClearFlagTimeout);
				iClearFlagTimeout = null;
			}
		}
		iOrientationTimeout = null;
	}

	function clearFlags(){
		bOrientationchange = false;
		bResize = false;
		iClearFlagTimeout = null;
	}

//******** Update browser settings for test purposes ********

	device._update = function(_simMobileOnDesktop) {
		ua = navigator.userAgent;
		logger.log(WARNING, "Device API values manipulated: NOT PRODUCTIVE FEATURE!!! This should be only used for test purposes. Only use if you know what you are doing.");
		setBrowser();
		setOS();
		setSystem(_simMobileOnDesktop);
	};

//********************************************************

	setResizeInfo(device.resize);
	setOrientationInfo(device.orientation);

	//Add API to global namespace
	window.sap.ui.Device = device;

	// Add handler for orientationchange and resize after initialization of Device API (IE8 fires onresize synchronously)
	if (device.support.touch && device.support.orientation) {
		//logic for mobile devices which support orientationchange (like ios, android, blackberry)
		window.addEventListener("resize", handleMobileOrientationResizeChange, false);
		window.addEventListener("orientationchange", handleMobileOrientationResizeChange, false);
	} else {
		if (window.addEventListener) {
			//most desktop browsers and windows phone/tablet which not support orientationchange
			window.addEventListener("resize", handleOrientationResizeChange, false);
		} else {
			//IE8
			window.attachEvent("onresize", handleOrientationResizeChange);
		}
	}

	//Always initialize the default media range set
	device.media.initRangeSet();
	device.media.initRangeSet(RANGESETS["SAP_STANDARD_EXTENDED"]);

	// define module if API is available
	if (sap.ui.define) {
		sap.ui.define("sap/ui/Device", [], function() {
			return device;
		});
	}

}());
/*!
 * URI.js - Mutating URLs
 *
 * Version: 1.11.2
 *
 * Author: Rodney Rehm
 * Web: http://medialize.github.com/URI.js/
 *
 * Licensed under
 *   MIT License http://www.opensource.org/licenses/mit-license
 *   GPL v3 http://opensource.org/licenses/GPL-3.0
 *
 */
(function (root, factory) {
    // https://github.com/umdjs/umd/blob/master/returnExports.js
    if (typeof exports === 'object') {
        // Node
        module.exports = factory(require('./punycode'), require('./IPv6'), require('./SecondLevelDomains'));
    } else if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
      // ##### BEGIN: MODIFIED BY SAP
      // define(['./punycode', './IPv6', './SecondLevelDomains'], factory);
      // we can't support loading URI.js via AMD define. URI.js is packaged with SAPUI5 code
      // and define() doesn't execute synchronously. So the UI5 code executed after URI.js
      // fails as it is missing the URI.js code.
      // Instead we use the standard init code and only expose the result via define()
      // The (optional) dependencies are lost or must be loaded in advance
      root.URI = factory(root.punycode, root.IPv6, root.SecondLevelDomains, root);
      define('sap/ui/thirdparty/URI', [], function() { return root.URI; });
      // ##### END: MODIFIED BY SAP
    } else {
        // Browser globals (root is window)
        root.URI = factory(root.punycode, root.IPv6, root.SecondLevelDomains, root);
    }
}(this, function (punycode, IPv6, SLD, root) {
"use strict";

// save current URI variable, if any
var _URI = root && root.URI;

function URI(url, base) {
    // Allow instantiation without the 'new' keyword
    if (!(this instanceof URI)) {
        return new URI(url, base);
    }

    if (url === undefined) {
        if (typeof location !== 'undefined') {
            url = location.href + "";
        } else {
            url = "";
        }
    }

    this.href(url);

    // resolve to base according to http://dvcs.w3.org/hg/url/raw-file/tip/Overview.html#constructor
    if (base !== undefined) {
        return this.absoluteTo(base);
    }

    return this;
};

var p = URI.prototype;
var hasOwn = Object.prototype.hasOwnProperty;

function escapeRegEx(string) {
    // https://github.com/medialize/URI.js/commit/85ac21783c11f8ccab06106dba9735a31a86924d#commitcomment-821963
    return string.replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$1');
}

function getType(value) {
    // IE8 doesn't return [Object Undefined] but [Object Object] for undefined value
    if (value === undefined) {
        return 'Undefined';
    }

    return String(Object.prototype.toString.call(value)).slice(8, -1);
}

function isArray(obj) {
    return getType(obj) === "Array";
}

function filterArrayValues(data, value) {
    var lookup = {};
    var i, length;

    if (isArray(value)) {
        for (i = 0, length = value.length; i < length; i++) {
            lookup[value[i]] = true;
        }
    } else {
        lookup[value] = true;
    }

    for (i = 0, length = data.length; i < length; i++) {
        if (lookup[data[i]] !== undefined) {
            data.splice(i, 1);
            length--;
            i--;
        }
    }

    return data;
}

function arrayContains(list, value) {
    var i, length;

    // value may be string, number, array, regexp
    if (isArray(value)) {
        // Note: this can be optimized to O(n) (instead of current O(m * n))
        for (i = 0, length = value.length; i < length; i++) {
            if (!arrayContains(list, value[i])) {
                return false;
            }
        }

        return true;
    }

    var _type = getType(value);
    for (i = 0, length = list.length; i < length; i++) {
        if (_type === 'RegExp') {
            if (typeof list[i] === 'string' && list[i].match(value)) {
                return true;
            }
        } else if (list[i] === value) {
            return true;
        }
    }

    return false;
}

function arraysEqual(one, two) {
    if (!isArray(one) || !isArray(two)) {
        return false;
    }

    // arrays can't be equal if they have different amount of content
    if (one.length !== two.length) {
        return false;
    }

    one.sort();
    two.sort();

    for (var i = 0, l = one.length; i < l; i++) {
        if (one[i] !== two[i]) {
            return false;
        }
    }

    return true;
}

URI._parts = function() {
    return {
        protocol: null,
        username: null,
        password: null,
        hostname: null,
        urn: null,
        port: null,
        path: null,
        query: null,
        fragment: null,
        // state
        duplicateQueryParameters: URI.duplicateQueryParameters,
        escapeQuerySpace: URI.escapeQuerySpace
    };
};
// state: allow duplicate query parameters (a=1&a=1)
URI.duplicateQueryParameters = false;
// state: replaces + with %20 (space in query strings)
URI.escapeQuerySpace = true;
// static properties
URI.protocol_expression = /^[a-z][a-z0-9-+-]*$/i;
URI.idn_expression = /[^a-z0-9\.-]/i;
URI.punycode_expression = /(xn--)/i;
// well, 333.444.555.666 matches, but it sure ain't no IPv4 - do we care?
URI.ip4_expression = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
// credits to Rich Brown
// source: http://forums.intermapper.com/viewtopic.php?p=1096#1096
// specification: http://www.ietf.org/rfc/rfc4291.txt
URI.ip6_expression = /^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;
// gruber revised expression - http://rodneyrehm.de/t/url-regex.html
URI.find_uri_expression = /\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))/ig;
// http://www.iana.org/assignments/uri-schemes.html
// http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports
URI.defaultPorts = {
    http: "80",
    https: "443",
    ftp: "21",
    gopher: "70",
    ws: "80",
    wss: "443"
};
// allowed hostname characters according to RFC 3986
// ALPHA DIGIT "-" "." "_" "~" "!" "$" "&" "'" "(" ")" "*" "+" "," ";" "=" %encoded
// I've never seen a (non-IDN) hostname other than: ALPHA DIGIT . -
URI.invalid_hostname_characters = /[^a-zA-Z0-9\.-]/;
// map DOM Elements to their URI attribute
URI.domAttributes = {
    'a': 'href',
    'blockquote': 'cite',
    'link': 'href',
    'base': 'href',
    'script': 'src',
    'form': 'action',
    'img': 'src',
    'area': 'href',
    'iframe': 'src',
    'embed': 'src',
    'source': 'src',
    'track': 'src',
    'input': 'src' // but only if type="image"
};
URI.getDomAttribute = function(node) {
    if (!node || !node.nodeName) {
        return undefined;
    }

    var nodeName = node.nodeName.toLowerCase();
    // <input> should only expose src for type="image"
    if (nodeName === 'input' && node.type !== 'image') {
        return undefined;
    }

    return URI.domAttributes[nodeName];
};

function escapeForDumbFirefox36(value) {
    // https://github.com/medialize/URI.js/issues/91
    return escape(value);
}

// encoding / decoding according to RFC3986
function strictEncodeURIComponent(string) {
    // see https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/encodeURIComponent
    return encodeURIComponent(string)
        .replace(/[!'()*]/g, escapeForDumbFirefox36)
        .replace(/\*/g, "%2A");
}
URI.encode = strictEncodeURIComponent;
URI.decode = decodeURIComponent;
URI.iso8859 = function() {
    URI.encode = escape;
    URI.decode = unescape;
};
URI.unicode = function() {
    URI.encode = strictEncodeURIComponent;
    URI.decode = decodeURIComponent;
};
URI.characters = {
    pathname: {
        encode: {
            // RFC3986 2.1: For consistency, URI producers and normalizers should
            // use uppercase hexadecimal digits for all percent-encodings.
            expression: /%(24|26|2B|2C|3B|3D|3A|40)/ig,
            map: {
                // -._~!'()*
                "%24": "$",
                "%26": "&",
                "%2B": "+",
                "%2C": ",",
                "%3B": ";",
                "%3D": "=",
                "%3A": ":",
                "%40": "@"
            }
        },
        decode: {
            expression: /[\/\?#]/g,
            map: {
                "/": "%2F",
                "?": "%3F",
                "#": "%23"
            }
        }
    },
    reserved: {
        encode: {
            // RFC3986 2.1: For consistency, URI producers and normalizers should
            // use uppercase hexadecimal digits for all percent-encodings.
            expression: /%(21|23|24|26|27|28|29|2A|2B|2C|2F|3A|3B|3D|3F|40|5B|5D)/ig,
            map: {
                // gen-delims
                "%3A": ":",
                "%2F": "/",
                "%3F": "?",
                "%23": "#",
                "%5B": "[",
                "%5D": "]",
                "%40": "@",
                // sub-delims
                "%21": "!",
                "%24": "$",
                "%26": "&",
                "%27": "'",
                "%28": "(",
                "%29": ")",
                "%2A": "*",
                "%2B": "+",
                "%2C": ",",
                "%3B": ";",
                "%3D": "="
            }
        }
    }
};
URI.encodeQuery = function(string, escapeQuerySpace) {
    var escaped = URI.encode(string + "");
    return escapeQuerySpace ? escaped.replace(/%20/g, '+') : escaped;
};
URI.decodeQuery = function(string, escapeQuerySpace) {
    string += "";
    try {
        return URI.decode(escapeQuerySpace ? string.replace(/\+/g, '%20') : string);
    } catch(e) {
        // we're not going to mess with weird encodings,
        // give up and return the undecoded original string
        // see https://github.com/medialize/URI.js/issues/87
        // see https://github.com/medialize/URI.js/issues/92
        return string;
    }
};
URI.recodePath = function(string) {
    var segments = (string + "").split('/');
    for (var i = 0, length = segments.length; i < length; i++) {
        segments[i] = URI.encodePathSegment(URI.decode(segments[i]));
    }

    return segments.join('/');
};
URI.decodePath = function(string) {
    var segments = (string + "").split('/');
    for (var i = 0, length = segments.length; i < length; i++) {
        segments[i] = URI.decodePathSegment(segments[i]);
    }

    return segments.join('/');
};
// generate encode/decode path functions
var _parts = {'encode':'encode', 'decode':'decode'};
var _part;
var generateAccessor = function(_group, _part) {
    return function(string) {
        return URI[_part](string + "").replace(URI.characters[_group][_part].expression, function(c) {
            return URI.characters[_group][_part].map[c];
        });
    };
};

for (_part in _parts) {
    URI[_part + "PathSegment"] = generateAccessor("pathname", _parts[_part]);
}

URI.encodeReserved = generateAccessor("reserved", "encode");

URI.parse = function(string, parts) {
    var pos;
    if (!parts) {
        parts = {};
    }
    // [protocol"://"[username[":"password]"@"]hostname[":"port]"/"?][path]["?"querystring]["#"fragment]

    // extract fragment
    pos = string.indexOf('#');
    if (pos > -1) {
        // escaping?
        parts.fragment = string.substring(pos + 1) || null;
        string = string.substring(0, pos);
    }

    // extract query
    pos = string.indexOf('?');
    if (pos > -1) {
        // escaping?
        parts.query = string.substring(pos + 1) || null;
        string = string.substring(0, pos);
    }

    // extract protocol
    if (string.substring(0, 2) === '//') {
        // relative-scheme
        parts.protocol = null;
        string = string.substring(2);
        // extract "user:pass@host:port"
        string = URI.parseAuthority(string, parts);
    } else {
        pos = string.indexOf(':');
        if (pos > -1) {
            parts.protocol = string.substring(0, pos) || null;
            if (parts.protocol && !parts.protocol.match(URI.protocol_expression)) {
                // : may be within the path
                parts.protocol = undefined;
            } else if (parts.protocol === 'file') {
                // the file scheme: does not contain an authority
                string = string.substring(pos + 3);
            } else if (string.substring(pos + 1, pos + 3) === '//') {
                string = string.substring(pos + 3);

                // extract "user:pass@host:port"
                string = URI.parseAuthority(string, parts);
            } else {
                string = string.substring(pos + 1);
                parts.urn = true;
            }
        }
    }

    // what's left must be the path
    parts.path = string;

    // and we're done
    return parts;
};
URI.parseHost = function(string, parts) {
    // extract host:port
    var pos = string.indexOf('/');
    var bracketPos;
    var t;

    if (pos === -1) {
        pos = string.length;
    }

    if (string.charAt(0) === "[") {
        // IPv6 host - http://tools.ietf.org/html/draft-ietf-6man-text-addr-representation-04#section-6
        // I claim most client software breaks on IPv6 anyways. To simplify things, URI only accepts
        // IPv6+port in the format [2001:db8::1]:80 (for the time being)
        bracketPos = string.indexOf(']');
        parts.hostname = string.substring(1, bracketPos) || null;
        parts.port = string.substring(bracketPos+2, pos) || null;
    } else if (string.indexOf(':') !== string.lastIndexOf(':')) {
        // IPv6 host contains multiple colons - but no port
        // this notation is actually not allowed by RFC 3986, but we're a liberal parser
        parts.hostname = string.substring(0, pos) || null;
        parts.port = null;
    } else {
        t = string.substring(0, pos).split(':');
        parts.hostname = t[0] || null;
        parts.port = t[1] || null;
    }

    if (parts.hostname && string.substring(pos).charAt(0) !== '/') {
        pos++;
        string = "/" + string;
    }

    return string.substring(pos) || '/';
};
URI.parseAuthority = function(string, parts) {
    string = URI.parseUserinfo(string, parts);
    return URI.parseHost(string, parts);
};
URI.parseUserinfo = function(string, parts) {
    // extract username:password
    var firstSlash = string.indexOf('/');
    var pos = firstSlash > -1
        ? string.lastIndexOf('@', firstSlash)
        : string.indexOf('@');
    var t;

    // authority@ must come before /path
    if (pos > -1 && (firstSlash === -1 || pos < firstSlash)) {
        t = string.substring(0, pos).split(':');
        parts.username = t[0] ? URI.decode(t[0]) : null;
        t.shift();
        parts.password = t[0] ? URI.decode(t.join(':')) : null;
        string = string.substring(pos + 1);
    } else {
        parts.username = null;
        parts.password = null;
    }

    return string;
};
URI.parseQuery = function(string, escapeQuerySpace) {
    if (!string) {
        return {};
    }

    // throw out the funky business - "?"[name"="value"&"]+
    string = string.replace(/&+/g, '&').replace(/^\?*&*|&+$/g, '');

    if (!string) {
        return {};
    }

    var items = {};
    var splits = string.split('&');
    var length = splits.length;
    var v, name, value;

    for (var i = 0; i < length; i++) {
        v = splits[i].split('=');
        name = URI.decodeQuery(v.shift(), escapeQuerySpace);
        // no "=" is null according to http://dvcs.w3.org/hg/url/raw-file/tip/Overview.html#collect-url-parameters
        value = v.length ? URI.decodeQuery(v.join('='), escapeQuerySpace) : null;

        if (items[name]) {
            if (typeof items[name] === "string") {
                items[name] = [items[name]];
            }

            items[name].push(value);
        } else {
            items[name] = value;
        }
    }

    return items;
};

URI.build = function(parts) {
    var t = "";

    if (parts.protocol) {
        t += parts.protocol + ":";
    }

    if (!parts.urn && (t || parts.hostname)) {
        t += '//';
    }

    t += (URI.buildAuthority(parts) || '');

    if (typeof parts.path === "string") {
        if (parts.path.charAt(0) !== '/' && typeof parts.hostname === "string") {
            t += '/';
        }

        t += parts.path;
    }

    if (typeof parts.query === "string" && parts.query) {
        t += '?' + parts.query;
    }

    if (typeof parts.fragment === "string" && parts.fragment) {
        t += '#' + parts.fragment;
    }
    return t;
};
URI.buildHost = function(parts) {
    var t = "";

    if (!parts.hostname) {
        return "";
    } else if (URI.ip6_expression.test(parts.hostname)) {
        if (parts.port) {
            t += "[" + parts.hostname + "]:" + parts.port;
        } else {
            // don't know if we should always wrap IPv6 in []
            // the RFC explicitly says SHOULD, not MUST.
            t += parts.hostname;
        }
    } else {
        t += parts.hostname;
        if (parts.port) {
            t += ':' + parts.port;
        }
    }

    return t;
};
URI.buildAuthority = function(parts) {
    return URI.buildUserinfo(parts) + URI.buildHost(parts);
};
URI.buildUserinfo = function(parts) {
    var t = "";

    if (parts.username) {
        t += URI.encode(parts.username);

        if (parts.password) {
            t += ':' + URI.encode(parts.password);
        }

        t += "@";
    }

    return t;
};
URI.buildQuery = function(data, duplicateQueryParameters, escapeQuerySpace) {
    // according to http://tools.ietf.org/html/rfc3986 or http://labs.apache.org/webarch/uri/rfc/rfc3986.html
    // being »-._~!$&'()*+,;=:@/?« %HEX and alnum are allowed
    // the RFC explicitly states ?/foo being a valid use case, no mention of parameter syntax!
    // URI.js treats the query string as being application/x-www-form-urlencoded
    // see http://www.w3.org/TR/REC-html40/interact/forms.html#form-content-type

    var t = "";
    var unique, key, i, length;
    for (key in data) {
        if (hasOwn.call(data, key) && key) {
            if (isArray(data[key])) {
                unique = {};
                for (i = 0, length = data[key].length; i < length; i++) {
                    if (data[key][i] !== undefined && unique[data[key][i] + ""] === undefined) {
                        t += "&" + URI.buildQueryParameter(key, data[key][i], escapeQuerySpace);
                        if (duplicateQueryParameters !== true) {
                            unique[data[key][i] + ""] = true;
                        }
                    }
                }
            } else if (data[key] !== undefined) {
                t += '&' + URI.buildQueryParameter(key, data[key], escapeQuerySpace);
            }
        }
    }

    return t.substring(1);
};
URI.buildQueryParameter = function(name, value, escapeQuerySpace) {
    // http://www.w3.org/TR/REC-html40/interact/forms.html#form-content-type -- application/x-www-form-urlencoded
    // don't append "=" for null values, according to http://dvcs.w3.org/hg/url/raw-file/tip/Overview.html#url-parameter-serialization
    return URI.encodeQuery(name, escapeQuerySpace) + (value !== null ? "=" + URI.encodeQuery(value, escapeQuerySpace) : "");
};

URI.addQuery = function(data, name, value) {
    if (typeof name === "object") {
        for (var key in name) {
            if (hasOwn.call(name, key)) {
                URI.addQuery(data, key, name[key]);
            }
        }
    } else if (typeof name === "string") {
        if (data[name] === undefined) {
            data[name] = value;
            return;
        } else if (typeof data[name] === "string") {
            data[name] = [data[name]];
        }

        if (!isArray(value)) {
            value = [value];
        }

        data[name] = data[name].concat(value);
    } else {
        throw new TypeError("URI.addQuery() accepts an object, string as the name parameter");
    }
};
URI.removeQuery = function(data, name, value) {
    var i, length, key;

    if (isArray(name)) {
        for (i = 0, length = name.length; i < length; i++) {
            data[name[i]] = undefined;
        }
    } else if (typeof name === "object") {
        for (key in name) {
            if (hasOwn.call(name, key)) {
                URI.removeQuery(data, key, name[key]);
            }
        }
    } else if (typeof name === "string") {
        if (value !== undefined) {
            if (data[name] === value) {
                data[name] = undefined;
            } else if (isArray(data[name])) {
                data[name] = filterArrayValues(data[name], value);
            }
        } else {
            data[name] = undefined;
        }
    } else {
        throw new TypeError("URI.addQuery() accepts an object, string as the first parameter");
    }
};
URI.hasQuery = function(data, name, value, withinArray) {
    if (typeof name === "object") {
        for (var key in name) {
            if (hasOwn.call(name, key)) {
                if (!URI.hasQuery(data, key, name[key])) {
                    return false;
                }
            }
        }

        return true;
    } else if (typeof name !== "string") {
        throw new TypeError("URI.hasQuery() accepts an object, string as the name parameter");
    }

    switch (getType(value)) {
        case 'Undefined':
            // true if exists (but may be empty)
            return name in data; // data[name] !== undefined;

        case 'Boolean':
            // true if exists and non-empty
            var _booly = Boolean(isArray(data[name]) ? data[name].length : data[name]);
            return value === _booly;

        case 'Function':
            // allow complex comparison
            return !!value(data[name], name, data);

        case 'Array':
            if (!isArray(data[name])) {
                return false;
            }

            var op = withinArray ? arrayContains : arraysEqual;
            return op(data[name], value);

        case 'RegExp':
            if (!isArray(data[name])) {
                return Boolean(data[name] && data[name].match(value));
            }

            if (!withinArray) {
                return false;
            }

            return arrayContains(data[name], value);

        case 'Number':
            value = String(value);
            // omit break;
        case 'String':
            if (!isArray(data[name])) {
                return data[name] === value;
            }

            if (!withinArray) {
                return false;
            }

            return arrayContains(data[name], value);

        default:
            throw new TypeError("URI.hasQuery() accepts undefined, boolean, string, number, RegExp, Function as the value parameter");
    }
};


URI.commonPath = function(one, two) {
    var length = Math.min(one.length, two.length);
    var pos;

    // find first non-matching character
    for (pos = 0; pos < length; pos++) {
        if (one.charAt(pos) !== two.charAt(pos)) {
            pos--;
            break;
        }
    }

    if (pos < 1) {
        return one.charAt(0) === two.charAt(0) && one.charAt(0) === '/' ? '/' : '';
    }

    // revert to last /
    if (one.charAt(pos) !== '/' || two.charAt(pos) !== '/') {
        pos = one.substring(0, pos).lastIndexOf('/');
    }

    return one.substring(0, pos + 1);
};

URI.withinString = function(string, callback) {
    // expression used is "gruber revised" (@gruber v2) determined to be the best solution in
    // a regex sprint we did a couple of ages ago at
    // * http://mathiasbynens.be/demo/url-regex
    // * http://rodneyrehm.de/t/url-regex.html

    return string.replace(URI.find_uri_expression, callback);
};

URI.ensureValidHostname = function(v) {
    // Theoretically URIs allow percent-encoding in Hostnames (according to RFC 3986)
    // they are not part of DNS and therefore ignored by URI.js

    if (v.match(URI.invalid_hostname_characters)) {
        // test punycode
        if (!punycode) {
            throw new TypeError("Hostname '" + v + "' contains characters other than [A-Z0-9.-] and Punycode.js is not available");
        }

        if (punycode.toASCII(v).match(URI.invalid_hostname_characters)) {
            throw new TypeError("Hostname '" + v + "' contains characters other than [A-Z0-9.-]");
        }
    }
};

// noConflict
URI.noConflict = function(removeAll) {
    if (removeAll) {
        var unconflicted = {
            URI: this.noConflict()
        };

        if (URITemplate && typeof URITemplate.noConflict == "function") {
            unconflicted.URITemplate = URITemplate.noConflict();
        }

        if (IPv6 && typeof IPv6.noConflict == "function") {
            unconflicted.IPv6 = IPv6.noConflict();
        }

        if (SecondLevelDomains && typeof SecondLevelDomains.noConflict == "function") {
            unconflicted.SecondLevelDomains = SecondLevelDomains.noConflict();
        }

        return unconflicted;
    } else if (root.URI === this) {
        root.URI = _URI;
    }

    return this;
};

p.build = function(deferBuild) {
    if (deferBuild === true) {
        this._deferred_build = true;
    } else if (deferBuild === undefined || this._deferred_build) {
        this._string = URI.build(this._parts);
        this._deferred_build = false;
    }

    return this;
};

p.clone = function() {
    return new URI(this);
};

p.valueOf = p.toString = function() {
    return this.build(false)._string;
};

// generate simple accessors
_parts = {protocol: 'protocol', username: 'username', password: 'password', hostname: 'hostname',  port: 'port'};
generateAccessor = function(_part){
    return function(v, build) {
        if (v === undefined) {
            return this._parts[_part] || "";
        } else {
            this._parts[_part] = v || null;
            this.build(!build);
            return this;
        }
    };
};

for (_part in _parts) {
    p[_part] = generateAccessor(_parts[_part]);
}

// generate accessors with optionally prefixed input
_parts = {query: '?', fragment: '#'};
generateAccessor = function(_part, _key){
    return function(v, build) {
        if (v === undefined) {
            return this._parts[_part] || "";
        } else {
            if (v !== null) {
                v = v + "";
                if (v.charAt(0) === _key) {
                    v = v.substring(1);
                }
            }

            this._parts[_part] = v;
            this.build(!build);
            return this;
        }
    };
};

for (_part in _parts) {
    p[_part] = generateAccessor(_part, _parts[_part]);
}

// generate accessors with prefixed output
_parts = {search: ['?', 'query'], hash: ['#', 'fragment']};
generateAccessor = function(_part, _key){
    return function(v, build) {
        var t = this[_part](v, build);
        return typeof t === "string" && t.length ? (_key + t) : t;
    };
};

for (_part in _parts) {
    p[_part] = generateAccessor(_parts[_part][1], _parts[_part][0]);
}

p.pathname = function(v, build) {
    if (v === undefined || v === true) {
        var res = this._parts.path || (this._parts.hostname ? '/' : '');
        return v ? URI.decodePath(res) : res;
    } else {
        this._parts.path = v ? URI.recodePath(v) : "/";
        this.build(!build);
        return this;
    }
};
p.path = p.pathname;
p.href = function(href, build) {
    var key;

    if (href === undefined) {
        return this.toString();
    }

    this._string = "";
    this._parts = URI._parts();

    var _URI = href instanceof URI;
    var _object = typeof href === "object" && (href.hostname || href.path || href.pathname);
    if (href.nodeName) {
        var attribute = URI.getDomAttribute(href);
        href = href[attribute] || "";
        _object = false;
    }

    // window.location is reported to be an object, but it's not the sort
    // of object we're looking for:
    // * location.protocol ends with a colon
    // * location.query != object.search
    // * location.hash != object.fragment
    // simply serializing the unknown object should do the trick
    // (for location, not for everything...)
    if (!_URI && _object && href.pathname !== undefined) {
        href = href.toString();
    }

    if (typeof href === "string") {
        this._parts = URI.parse(href, this._parts);
    } else if (_URI || _object) {
        var src = _URI ? href._parts : href;
        for (key in src) {
            if (hasOwn.call(this._parts, key)) {
                this._parts[key] = src[key];
            }
        }
    } else {
        throw new TypeError("invalid input");
    }

    this.build(!build);
    return this;
};

// identification accessors
p.is = function(what) {
    var ip = false;
    var ip4 = false;
    var ip6 = false;
    var name = false;
    var sld = false;
    var idn = false;
    var punycode = false;
    var relative = !this._parts.urn;

    if (this._parts.hostname) {
        relative = false;
        ip4 = URI.ip4_expression.test(this._parts.hostname);
        ip6 = URI.ip6_expression.test(this._parts.hostname);
        ip = ip4 || ip6;
        name = !ip;
        sld = name && SLD && SLD.has(this._parts.hostname);
        idn = name && URI.idn_expression.test(this._parts.hostname);
        punycode = name && URI.punycode_expression.test(this._parts.hostname);
    }

    switch (what.toLowerCase()) {
        case 'relative':
            return relative;

        case 'absolute':
            return !relative;

        // hostname identification
        case 'domain':
        case 'name':
            return name;

        case 'sld':
            return sld;

        case 'ip':
            return ip;

        case 'ip4':
        case 'ipv4':
        case 'inet4':
            return ip4;

        case 'ip6':
        case 'ipv6':
        case 'inet6':
            return ip6;

        case 'idn':
            return idn;

        case 'url':
            return !this._parts.urn;

        case 'urn':
            return !!this._parts.urn;

        case 'punycode':
            return punycode;
    }

    return null;
};

// component specific input validation
var _protocol = p.protocol;
var _port = p.port;
var _hostname = p.hostname;

p.protocol = function(v, build) {
    if (v !== undefined) {
        if (v) {
            // accept trailing ://
            v = v.replace(/:(\/\/)?$/, '');

            if (v.match(/[^a-zA-z0-9\.+-]/)) {
                throw new TypeError("Protocol '" + v + "' contains characters other than [A-Z0-9.+-]");
            }
        }
    }
    return _protocol.call(this, v, build);
};
p.scheme = p.protocol;
p.port = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v !== undefined) {
        if (v === 0) {
            v = null;
        }

        if (v) {
            v += "";
            if (v.charAt(0) === ":") {
                v = v.substring(1);
            }

            if (v.match(/[^0-9]/)) {
                throw new TypeError("Port '" + v + "' contains characters other than [0-9]");
            }
        }
    }
    return _port.call(this, v, build);
};
p.hostname = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v !== undefined) {
        var x = {};
        URI.parseHost(v, x);
        v = x.hostname;
    }
    return _hostname.call(this, v, build);
};

// compound accessors
p.host = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v === undefined) {
        return this._parts.hostname ? URI.buildHost(this._parts) : "";
    } else {
        URI.parseHost(v, this._parts);
        this.build(!build);
        return this;
    }
};
p.authority = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v === undefined) {
        return this._parts.hostname ? URI.buildAuthority(this._parts) : "";
    } else {
        URI.parseAuthority(v, this._parts);
        this.build(!build);
        return this;
    }
};
p.userinfo = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v === undefined) {
        if (!this._parts.username) {
            return "";
        }

        var t = URI.buildUserinfo(this._parts);
        return t.substring(0, t.length -1);
    } else {
        if (v[v.length-1] !== '@') {
            v += '@';
        }

        URI.parseUserinfo(v, this._parts);
        this.build(!build);
        return this;
    }
};
p.resource = function(v, build) {
    var parts;

    if (v === undefined) {
        return this.path() + this.search() + this.hash();
    }

    parts = URI.parse(v);
    this._parts.path = parts.path;
    this._parts.query = parts.query;
    this._parts.fragment = parts.fragment;
    this.build(!build);
    return this;
};

// fraction accessors
p.subdomain = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    // convenience, return "www" from "www.example.org"
    if (v === undefined) {
        if (!this._parts.hostname || this.is('IP')) {
            return "";
        }

        // grab domain and add another segment
        var end = this._parts.hostname.length - this.domain().length - 1;
        return this._parts.hostname.substring(0, end) || "";
    } else {
        var e = this._parts.hostname.length - this.domain().length;
        var sub = this._parts.hostname.substring(0, e);
        var replace = new RegExp('^' + escapeRegEx(sub));

        if (v && v.charAt(v.length - 1) !== '.') {
            v += ".";
        }

        if (v) {
            URI.ensureValidHostname(v);
        }

        this._parts.hostname = this._parts.hostname.replace(replace, v);
        this.build(!build);
        return this;
    }
};
p.domain = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (typeof v === 'boolean') {
        build = v;
        v = undefined;
    }

    // convenience, return "example.org" from "www.example.org"
    if (v === undefined) {
        if (!this._parts.hostname || this.is('IP')) {
            return "";
        }

        // if hostname consists of 1 or 2 segments, it must be the domain
        var t = this._parts.hostname.match(/\./g);
        if (t && t.length < 2) {
            return this._parts.hostname;
        }

        // grab tld and add another segment
        var end = this._parts.hostname.length - this.tld(build).length - 1;
        end = this._parts.hostname.lastIndexOf('.', end -1) + 1;
        return this._parts.hostname.substring(end) || "";
    } else {
        if (!v) {
            throw new TypeError("cannot set domain empty");
        }

        URI.ensureValidHostname(v);

        if (!this._parts.hostname || this.is('IP')) {
            this._parts.hostname = v;
        } else {
            var replace = new RegExp(escapeRegEx(this.domain()) + "$");
            this._parts.hostname = this._parts.hostname.replace(replace, v);
        }

        this.build(!build);
        return this;
    }
};
p.tld = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (typeof v === 'boolean') {
        build = v;
        v = undefined;
    }

    // return "org" from "www.example.org"
    if (v === undefined) {
        if (!this._parts.hostname || this.is('IP')) {
            return "";
        }

        var pos = this._parts.hostname.lastIndexOf('.');
        var tld = this._parts.hostname.substring(pos + 1);

        if (build !== true && SLD && SLD.list[tld.toLowerCase()]) {
            return SLD.get(this._parts.hostname) || tld;
        }

        return tld;
    } else {
        var replace;

        if (!v) {
            throw new TypeError("cannot set TLD empty");
        } else if (v.match(/[^a-zA-Z0-9-]/)) {
            if (SLD && SLD.is(v)) {
                replace = new RegExp(escapeRegEx(this.tld()) + "$");
                this._parts.hostname = this._parts.hostname.replace(replace, v);
            } else {
                throw new TypeError("TLD '" + v + "' contains characters other than [A-Z0-9]");
            }
        } else if (!this._parts.hostname || this.is('IP')) {
            throw new ReferenceError("cannot set TLD on non-domain host");
        } else {
            replace = new RegExp(escapeRegEx(this.tld()) + "$");
            this._parts.hostname = this._parts.hostname.replace(replace, v);
        }

        this.build(!build);
        return this;
    }
};
p.directory = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v === undefined || v === true) {
        if (!this._parts.path && !this._parts.hostname) {
            return '';
        }

        if (this._parts.path === '/') {
            return '/';
        }

        var end = this._parts.path.length - this.filename().length - 1;
        var res = this._parts.path.substring(0, end) || (this._parts.hostname ? "/" : "");

        return v ? URI.decodePath(res) : res;

    } else {
        var e = this._parts.path.length - this.filename().length;
        var directory = this._parts.path.substring(0, e);
        var replace = new RegExp('^' + escapeRegEx(directory));

        // fully qualifier directories begin with a slash
        if (!this.is('relative')) {
            if (!v) {
                v = '/';
            }

            if (v.charAt(0) !== '/') {
                v = "/" + v;
            }
        }

        // directories always end with a slash
        if (v && v.charAt(v.length - 1) !== '/') {
            v += '/';
        }

        v = URI.recodePath(v);
        this._parts.path = this._parts.path.replace(replace, v);
        this.build(!build);
        return this;
    }
};
p.filename = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v === undefined || v === true) {
        if (!this._parts.path || this._parts.path === '/') {
            return "";
        }

        var pos = this._parts.path.lastIndexOf('/');
        var res = this._parts.path.substring(pos+1);

        return v ? URI.decodePathSegment(res) : res;
    } else {
        var mutatedDirectory = false;

        if (v.charAt(0) === '/') {
            v = v.substring(1);
        }

        if (v.match(/\.?\//)) {
            mutatedDirectory = true;
        }

        var replace = new RegExp(escapeRegEx(this.filename()) + "$");
        v = URI.recodePath(v);
        this._parts.path = this._parts.path.replace(replace, v);

        if (mutatedDirectory) {
            this.normalizePath(build);
        } else {
            this.build(!build);
        }

        return this;
    }
};
p.suffix = function(v, build) {
    if (this._parts.urn) {
        return v === undefined ? '' : this;
    }

    if (v === undefined || v === true) {
        if (!this._parts.path || this._parts.path === '/') {
            return "";
        }

        var filename = this.filename();
        var pos = filename.lastIndexOf('.');
        var s, res;

        if (pos === -1) {
            return "";
        }

        // suffix may only contain alnum characters (yup, I made this up.)
        s = filename.substring(pos+1);
        res = (/^[a-z0-9%]+$/i).test(s) ? s : "";
        return v ? URI.decodePathSegment(res) : res;
    } else {
        if (v.charAt(0) === '.') {
            v = v.substring(1);
        }

        var suffix = this.suffix();
        var replace;

        if (!suffix) {
            if (!v) {
                return this;
            }

            this._parts.path += '.' + URI.recodePath(v);
        } else if (!v) {
            replace = new RegExp(escapeRegEx("." + suffix) + "$");
        } else {
            replace = new RegExp(escapeRegEx(suffix) + "$");
        }

        if (replace) {
            v = URI.recodePath(v);
            this._parts.path = this._parts.path.replace(replace, v);
        }

        this.build(!build);
        return this;
    }
};
p.segment = function(segment, v, build) {
    var separator = this._parts.urn ? ':' : '/';
    var path = this.path();
    var absolute = path.substring(0, 1) === '/';
    var segments = path.split(separator);

    if (segment !== undefined && typeof segment !== 'number') {
        build = v;
        v = segment;
        segment = undefined;
    }

    if (segment !== undefined && typeof segment !== 'number') {
        throw new Error("Bad segment '" + segment + "', must be 0-based integer");
    }

    if (absolute) {
        segments.shift();
    }

    if (segment < 0) {
        // allow negative indexes to address from the end
        segment = Math.max(segments.length + segment, 0);
    }

    if (v === undefined) {
        return segment === undefined
            ? segments
            : segments[segment];
    } else if (segment === null || segments[segment] === undefined) {
        if (isArray(v)) {
            segments = [];
            // collapse empty elements within array
            for (var i=0, l=v.length; i < l; i++) {
                if (!v[i].length && (!segments.length || !segments[segments.length -1].length)) {
                    continue;
                }

                if (segments.length && !segments[segments.length -1].length) {
                    segments.pop();
                }

                segments.push(v[i]);
            }
        } else if (v || (typeof v === "string")) {
            if (segments[segments.length -1] === "") {
                // empty trailing elements have to be overwritten
                // to prevent results such as /foo//bar
                segments[segments.length -1] = v;
            } else {
                segments.push(v);
            }
        }
    } else {
        if (v || (typeof v === "string" && v.length)) {
            segments[segment] = v;
        } else {
            segments.splice(segment, 1);
        }
    }

    if (absolute) {
        segments.unshift("");
    }

    return this.path(segments.join(separator), build);
};
p.segmentCoded = function(segment, v, build) {
    var segments, i, l;

    if (typeof segment !== 'number') {
        build = v;
        v = segment;
        segment = undefined;
    }

    if (v === undefined) {
        segments = this.segment(segment, v, build);
        if (!isArray(segments)) {
            segments = segments !== undefined ? URI.decode(segments) : undefined;
        } else {
            for (i = 0, l = segments.length; i < l; i++) {
                segments[i] = URI.decode(segments[i]);
            }
        }

        return segments;
    }

    if (!isArray(v)) {
        v = typeof v === 'string' ? URI.encode(v) : v;
    } else {
        for (i = 0, l = v.length; i < l; i++) {
            v[i] = URI.decode(v[i]);
        }
    }

    return this.segment(segment, v, build);
};

// mutating query string
var q = p.query;
p.query = function(v, build) {
    if (v === true) {
        return URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace);
    } else if (typeof v === "function") {
        var data = URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace);
        var result = v.call(this, data);
        this._parts.query = URI.buildQuery(result || data, this._parts.duplicateQueryParameters, this._parts.escapeQuerySpace);
        this.build(!build);
        return this;
    } else if (v !== undefined && typeof v !== "string") {
        this._parts.query = URI.buildQuery(v, this._parts.duplicateQueryParameters, this._parts.escapeQuerySpace);
        this.build(!build);
        return this;
    } else {
        return q.call(this, v, build);
    }
};
p.setQuery = function(name, value, build) {
    var data = URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace);

    if (typeof name === "object") {
        for (var key in name) {
            if (hasOwn.call(name, key)) {
                data[key] = name[key];
            }
        }
    } else if (typeof name === "string") {
        data[name] = value !== undefined ? value : null;
    } else {
        throw new TypeError("URI.addQuery() accepts an object, string as the name parameter");
    }

    this._parts.query = URI.buildQuery(data, this._parts.duplicateQueryParameters, this._parts.escapeQuerySpace);
    if (typeof name !== "string") {
        build = value;
    }

    this.build(!build);
    return this;
};
p.addQuery = function(name, value, build) {
    var data = URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace);
    URI.addQuery(data, name, value === undefined ? null : value);
    this._parts.query = URI.buildQuery(data, this._parts.duplicateQueryParameters, this._parts.escapeQuerySpace);
    if (typeof name !== "string") {
        build = value;
    }

    this.build(!build);
    return this;
};
p.removeQuery = function(name, value, build) {
    var data = URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace);
    URI.removeQuery(data, name, value);
    this._parts.query = URI.buildQuery(data, this._parts.duplicateQueryParameters, this._parts.escapeQuerySpace);
    if (typeof name !== "string") {
        build = value;
    }

    this.build(!build);
    return this;
};
p.hasQuery = function(name, value, withinArray) {
    var data = URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace);
    return URI.hasQuery(data, name, value, withinArray);
};
p.setSearch = p.setQuery;
p.addSearch = p.addQuery;
p.removeSearch = p.removeQuery;
p.hasSearch = p.hasQuery;

// sanitizing URLs
p.normalize = function() {
    if (this._parts.urn) {
        return this
            .normalizeProtocol(false)
            .normalizeQuery(false)
            .normalizeFragment(false)
            .build();
    }

    return this
        .normalizeProtocol(false)
        .normalizeHostname(false)
        .normalizePort(false)
        .normalizePath(false)
        .normalizeQuery(false)
        .normalizeFragment(false)
        .build();
};
p.normalizeProtocol = function(build) {
    if (typeof this._parts.protocol === "string") {
        this._parts.protocol = this._parts.protocol.toLowerCase();
        this.build(!build);
    }

    return this;
};
p.normalizeHostname = function(build) {
    if (this._parts.hostname) {
        if (this.is('IDN') && punycode) {
            this._parts.hostname = punycode.toASCII(this._parts.hostname);
        } else if (this.is('IPv6') && IPv6) {
            this._parts.hostname = IPv6.best(this._parts.hostname);
        }

        this._parts.hostname = this._parts.hostname.toLowerCase();
        this.build(!build);
    }

    return this;
};
p.normalizePort = function(build) {
    // remove port of it's the protocol's default
    if (typeof this._parts.protocol === "string" && this._parts.port === URI.defaultPorts[this._parts.protocol]) {
        this._parts.port = null;
        this.build(!build);
    }

    return this;
};
p.normalizePath = function(build) {
    if (this._parts.urn) {
        return this;
    }

    if (!this._parts.path || this._parts.path === '/') {
        return this;
    }

    var _was_relative;
    var _path = this._parts.path;
    var _parent, _pos;

    // handle relative paths
    if (_path.charAt(0) !== '/') {
        _was_relative = true;
        _path = '/' + _path;
    }

    // resolve simples
    _path = _path
        .replace(/(\/(\.\/)+)|(\/\.$)/g, '/')
        .replace(/\/{2,}/g, '/');

    // resolve parents
    while (true) {
        _parent = _path.indexOf('/../');
        if (_parent === -1) {
            // no more ../ to resolve
            break;
        } else if (_parent === 0) {
            // top level cannot be relative...
            _path = _path.substring(3);
            break;
        }

        _pos = _path.substring(0, _parent).lastIndexOf('/');
        if (_pos === -1) {
            _pos = _parent;
        }
        _path = _path.substring(0, _pos) + _path.substring(_parent + 3);
    }

    // revert to relative
    if (_was_relative && this.is('relative')) {
        _path = _path.substring(1);
    }

    _path = URI.recodePath(_path);
    this._parts.path = _path;
    this.build(!build);
    return this;
};
p.normalizePathname = p.normalizePath;
p.normalizeQuery = function(build) {
    if (typeof this._parts.query === "string") {
        if (!this._parts.query.length) {
            this._parts.query = null;
        } else {
            this.query(URI.parseQuery(this._parts.query, this._parts.escapeQuerySpace));
        }

        this.build(!build);
    }

    return this;
};
p.normalizeFragment = function(build) {
    if (!this._parts.fragment) {
        this._parts.fragment = null;
        this.build(!build);
    }

    return this;
};
p.normalizeSearch = p.normalizeQuery;
p.normalizeHash = p.normalizeFragment;

p.iso8859 = function() {
    // expect unicode input, iso8859 output
    var e = URI.encode;
    var d = URI.decode;

    URI.encode = escape;
    URI.decode = decodeURIComponent;
    this.normalize();
    URI.encode = e;
    URI.decode = d;
    return this;
};

p.unicode = function() {
    // expect iso8859 input, unicode output
    var e = URI.encode;
    var d = URI.decode;

    URI.encode = strictEncodeURIComponent;
    URI.decode = unescape;
    this.normalize();
    URI.encode = e;
    URI.decode = d;
    return this;
};

p.readable = function() {
    var uri = this.clone();
    // removing username, password, because they shouldn't be displayed according to RFC 3986
    uri.username("").password("").normalize();
    var t = '';
    if (uri._parts.protocol) {
        t += uri._parts.protocol + '://';
    }

    if (uri._parts.hostname) {
        if (uri.is('punycode') && punycode) {
            t += punycode.toUnicode(uri._parts.hostname);
            if (uri._parts.port) {
                t += ":" + uri._parts.port;
            }
        } else {
            t += uri.host();
        }
    }

    if (uri._parts.hostname && uri._parts.path && uri._parts.path.charAt(0) !== '/') {
        t += '/';
    }

    t += uri.path(true);
    if (uri._parts.query) {
        var q = '';
        for (var i = 0, qp = uri._parts.query.split('&'), l = qp.length; i < l; i++) {
            var kv = (qp[i] || "").split('=');
            q += '&' + URI.decodeQuery(kv[0], this._parts.escapeQuerySpace)
                .replace(/&/g, '%26');

            if (kv[1] !== undefined) {
                q += "=" + URI.decodeQuery(kv[1], this._parts.escapeQuerySpace)
                    .replace(/&/g, '%26');
            }
        }
        t += '?' + q.substring(1);
    }

    t += URI.decodeQuery(uri.hash(), true);
    return t;
};

// resolving relative and absolute URLs
p.absoluteTo = function(base) {
    var resolved = this.clone();
    var properties = ['protocol', 'username', 'password', 'hostname', 'port'];
    var basedir, i, p;

    if (this._parts.urn) {
        throw new Error('URNs do not have any generally defined hierarchical components');
    }

    if (!(base instanceof URI)) {
        base = new URI(base);
    }

    if (!resolved._parts.protocol) {
        resolved._parts.protocol = base._parts.protocol;
    }

    if (this._parts.hostname) {
        return resolved;
    }

    for (i = 0; p = properties[i]; i++) {
        resolved._parts[p] = base._parts[p];
    }

    properties = ['query', 'path'];
    for (i = 0; p = properties[i]; i++) {
        if (!resolved._parts[p] && base._parts[p]) {
            resolved._parts[p] = base._parts[p];
        }
    }

    if (resolved.path().charAt(0) !== '/') {
        basedir = base.directory();
        resolved._parts.path = (basedir ? (basedir + '/') : '') + resolved._parts.path;
        resolved.normalizePath();
    }

    resolved.build();
    return resolved;
};
p.relativeTo = function(base) {
    var relative = this.clone().normalize();
    var relativeParts, baseParts, common, relativePath, basePath;

    if (relative._parts.urn) {
        throw new Error('URNs do not have any generally defined hierarchical components');
    }

    base = new URI(base).normalize();
    relativeParts = relative._parts;
    baseParts = base._parts;
    relativePath = relative.path();
    basePath = base.path();

    if (relativePath.charAt(0) !== '/') {
        throw new Error('URI is already relative');
    }

    if (basePath.charAt(0) !== '/') {
        throw new Error('Cannot calculate a URI relative to another relative URI');
    }

    if (relativeParts.protocol === baseParts.protocol) {
        relativeParts.protocol = null;
    }

    if (relativeParts.username !== baseParts.username || relativeParts.password !== baseParts.password) {
        return relative.build();
    }

    if (relativeParts.protocol !== null || relativeParts.username !== null || relativeParts.password !== null) {
        return relative.build();
    }

    if (relativeParts.hostname === baseParts.hostname && relativeParts.port === baseParts.port) {
        relativeParts.hostname = null;
        relativeParts.port = null;
    } else {
        return relative.build();
    }

    if (relativePath === basePath) {
        relativeParts.path = '';
        return relative.build();
    }

    // determine common sub path
    common = URI.commonPath(relative.path(), base.path());

    // If the paths have nothing in common, return a relative URL with the absolute path.
    if (!common) {
        return relative.build();
    }

    var parents = baseParts.path
        .substring(common.length)
        .replace(/[^\/]*$/, '')
        .replace(/.*?\//g, '../');

    relativeParts.path = parents + relativeParts.path.substring(common.length);

    return relative.build();
};

// comparing URIs
p.equals = function(uri) {
    var one = this.clone();
    var two = new URI(uri);
    var one_map = {};
    var two_map = {};
    var checked = {};
    var one_query, two_query, key;

    one.normalize();
    two.normalize();

    // exact match
    if (one.toString() === two.toString()) {
        return true;
    }

    // extract query string
    one_query = one.query();
    two_query = two.query();
    one.query("");
    two.query("");

    // definitely not equal if not even non-query parts match
    if (one.toString() !== two.toString()) {
        return false;
    }

    // query parameters have the same length, even if they're permuted
    if (one_query.length !== two_query.length) {
        return false;
    }

    one_map = URI.parseQuery(one_query, this._parts.escapeQuerySpace);
    two_map = URI.parseQuery(two_query, this._parts.escapeQuerySpace);

    for (key in one_map) {
        if (hasOwn.call(one_map, key)) {
            if (!isArray(one_map[key])) {
                if (one_map[key] !== two_map[key]) {
                    return false;
                }
            } else if (!arraysEqual(one_map[key], two_map[key])) {
                return false;
            }

            checked[key] = true;
        }
    }

    for (key in two_map) {
        if (hasOwn.call(two_map, key)) {
            if (!checked[key]) {
                // two contains a parameter not present in one
                return false;
            }
        }
    }

    return true;
};

// state
p.duplicateQueryParameters = function(v) {
    this._parts.duplicateQueryParameters = !!v;
    return this;
};

p.escapeQuerySpace = function(v) {
    this._parts.escapeQuerySpace = !!v;
    return this;
};

return URI;
}));
/*!
 * @overview es6-promise - a tiny implementation of Promises/A+.
 * @copyright Copyright (c) 2014 Yehuda Katz, Tom Dale, Stefan Penner and contributors (Conversion to ES6 API by Jake Archibald)
 * @license   Licensed under MIT license
 *            See https://raw.githubusercontent.com/jakearchibald/es6-promise/master/LICENSE
 * @version   2.3.0
 */

(function() {
    "use strict";
    function lib$es6$promise$utils$$objectOrFunction(x) {
      return typeof x === 'function' || (typeof x === 'object' && x !== null);
    }

    function lib$es6$promise$utils$$isFunction(x) {
      return typeof x === 'function';
    }

    function lib$es6$promise$utils$$isMaybeThenable(x) {
      return typeof x === 'object' && x !== null;
    }

    var lib$es6$promise$utils$$_isArray;
    if (!Array.isArray) {
      lib$es6$promise$utils$$_isArray = function (x) {
        return Object.prototype.toString.call(x) === '[object Array]';
      };
    } else {
      lib$es6$promise$utils$$_isArray = Array.isArray;
    }

    var lib$es6$promise$utils$$isArray = lib$es6$promise$utils$$_isArray;
    var lib$es6$promise$asap$$len = 0;
    var lib$es6$promise$asap$$toString = {}.toString;
    var lib$es6$promise$asap$$vertxNext;
    var lib$es6$promise$asap$$customSchedulerFn;

    var lib$es6$promise$asap$$asap = function asap(callback, arg) {
      lib$es6$promise$asap$$queue[lib$es6$promise$asap$$len] = callback;
      lib$es6$promise$asap$$queue[lib$es6$promise$asap$$len + 1] = arg;
      lib$es6$promise$asap$$len += 2;
      if (lib$es6$promise$asap$$len === 2) {
        // If len is 2, that means that we need to schedule an async flush.
        // If additional callbacks are queued before the queue is flushed, they
        // will be processed by this flush that we are scheduling.
        if (lib$es6$promise$asap$$customSchedulerFn) {
          lib$es6$promise$asap$$customSchedulerFn(lib$es6$promise$asap$$flush);
        } else {
          lib$es6$promise$asap$$scheduleFlush();
        }
      }
    }

    function lib$es6$promise$asap$$setScheduler(scheduleFn) {
      lib$es6$promise$asap$$customSchedulerFn = scheduleFn;
    }

    function lib$es6$promise$asap$$setAsap(asapFn) {
      lib$es6$promise$asap$$asap = asapFn;
    }

    var lib$es6$promise$asap$$browserWindow = (typeof window !== 'undefined') ? window : undefined;
    var lib$es6$promise$asap$$browserGlobal = lib$es6$promise$asap$$browserWindow || {};
    var lib$es6$promise$asap$$BrowserMutationObserver = lib$es6$promise$asap$$browserGlobal.MutationObserver || lib$es6$promise$asap$$browserGlobal.WebKitMutationObserver;
    var lib$es6$promise$asap$$isNode = typeof process !== 'undefined' && {}.toString.call(process) === '[object process]';

    // test for web worker but not in IE10
    var lib$es6$promise$asap$$isWorker = typeof Uint8ClampedArray !== 'undefined' &&
      typeof importScripts !== 'undefined' &&
      typeof MessageChannel !== 'undefined';

    // node
    function lib$es6$promise$asap$$useNextTick() {
      var nextTick = process.nextTick;
      // node version 0.10.x displays a deprecation warning when nextTick is used recursively
      // setImmediate should be used instead instead
      var version = process.versions.node.match(/^(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)$/);
      if (Array.isArray(version) && version[1] === '0' && version[2] === '10') {
        nextTick = setImmediate;
      }
      return function() {
        nextTick(lib$es6$promise$asap$$flush);
      };
    }

    // vertx
    function lib$es6$promise$asap$$useVertxTimer() {
      return function() {
        lib$es6$promise$asap$$vertxNext(lib$es6$promise$asap$$flush);
      };
    }

    function lib$es6$promise$asap$$useMutationObserver() {
      var iterations = 0;
      var observer = new lib$es6$promise$asap$$BrowserMutationObserver(lib$es6$promise$asap$$flush);
      var node = document.createTextNode('');
      observer.observe(node, { characterData: true });

      return function() {
        node.data = (iterations = ++iterations % 2);
      };
    }

    // web worker
    function lib$es6$promise$asap$$useMessageChannel() {
      var channel = new MessageChannel();
      channel.port1.onmessage = lib$es6$promise$asap$$flush;
      return function () {
        channel.port2.postMessage(0);
      };
    }

    function lib$es6$promise$asap$$useSetTimeout() {
      return function() {
        setTimeout(lib$es6$promise$asap$$flush, 1);
      };
    }

    var lib$es6$promise$asap$$queue = new Array(1000);
    function lib$es6$promise$asap$$flush() {
      for (var i = 0; i < lib$es6$promise$asap$$len; i+=2) {
        var callback = lib$es6$promise$asap$$queue[i];
        var arg = lib$es6$promise$asap$$queue[i+1];

        callback(arg);

        lib$es6$promise$asap$$queue[i] = undefined;
        lib$es6$promise$asap$$queue[i+1] = undefined;
      }

      lib$es6$promise$asap$$len = 0;
    }

    function lib$es6$promise$asap$$attemptVertex() {
      try {
        var r = require;
        var vertx = r('vertx');
        lib$es6$promise$asap$$vertxNext = vertx.runOnLoop || vertx.runOnContext;
        return lib$es6$promise$asap$$useVertxTimer();
      } catch(e) {
        return lib$es6$promise$asap$$useSetTimeout();
      }
    }

    var lib$es6$promise$asap$$scheduleFlush;
    // Decide what async method to use to triggering processing of queued callbacks:
    if (lib$es6$promise$asap$$isNode) {
      lib$es6$promise$asap$$scheduleFlush = lib$es6$promise$asap$$useNextTick();
    } else if (lib$es6$promise$asap$$BrowserMutationObserver) {
      lib$es6$promise$asap$$scheduleFlush = lib$es6$promise$asap$$useMutationObserver();
    } else if (lib$es6$promise$asap$$isWorker) {
      lib$es6$promise$asap$$scheduleFlush = lib$es6$promise$asap$$useMessageChannel();
    } else if (lib$es6$promise$asap$$browserWindow === undefined && typeof require === 'function') {
      lib$es6$promise$asap$$scheduleFlush = lib$es6$promise$asap$$attemptVertex();
    } else {
      lib$es6$promise$asap$$scheduleFlush = lib$es6$promise$asap$$useSetTimeout();
    }

    function lib$es6$promise$$internal$$noop() {}

    var lib$es6$promise$$internal$$PENDING   = void 0;
    var lib$es6$promise$$internal$$FULFILLED = 1;
    var lib$es6$promise$$internal$$REJECTED  = 2;

    var lib$es6$promise$$internal$$GET_THEN_ERROR = new lib$es6$promise$$internal$$ErrorObject();

    function lib$es6$promise$$internal$$selfFullfillment() {
      return new TypeError("You cannot resolve a promise with itself");
    }

    function lib$es6$promise$$internal$$cannotReturnOwn() {
      return new TypeError('A promises callback cannot return that same promise.');
    }

    function lib$es6$promise$$internal$$getThen(promise) {
      try {
        return promise.then;
      } catch(error) {
        lib$es6$promise$$internal$$GET_THEN_ERROR.error = error;
        return lib$es6$promise$$internal$$GET_THEN_ERROR;
      }
    }

    function lib$es6$promise$$internal$$tryThen(then, value, fulfillmentHandler, rejectionHandler) {
      try {
        then.call(value, fulfillmentHandler, rejectionHandler);
      } catch(e) {
        return e;
      }
    }

    function lib$es6$promise$$internal$$handleForeignThenable(promise, thenable, then) {
       lib$es6$promise$asap$$asap(function(promise) {
        var sealed = false;
        var error = lib$es6$promise$$internal$$tryThen(then, thenable, function(value) {
          if (sealed) { return; }
          sealed = true;
          if (thenable !== value) {
            lib$es6$promise$$internal$$resolve(promise, value);
          } else {
            lib$es6$promise$$internal$$fulfill(promise, value);
          }
        }, function(reason) {
          if (sealed) { return; }
          sealed = true;

          lib$es6$promise$$internal$$reject(promise, reason);
        }, 'Settle: ' + (promise._label || ' unknown promise'));

        if (!sealed && error) {
          sealed = true;
          lib$es6$promise$$internal$$reject(promise, error);
        }
      }, promise);
    }

    function lib$es6$promise$$internal$$handleOwnThenable(promise, thenable) {
      if (thenable._state === lib$es6$promise$$internal$$FULFILLED) {
        lib$es6$promise$$internal$$fulfill(promise, thenable._result);
      } else if (thenable._state === lib$es6$promise$$internal$$REJECTED) {
        lib$es6$promise$$internal$$reject(promise, thenable._result);
      } else {
        lib$es6$promise$$internal$$subscribe(thenable, undefined, function(value) {
          lib$es6$promise$$internal$$resolve(promise, value);
        }, function(reason) {
          lib$es6$promise$$internal$$reject(promise, reason);
        });
      }
    }

    function lib$es6$promise$$internal$$handleMaybeThenable(promise, maybeThenable) {
      if (maybeThenable.constructor === promise.constructor) {
        lib$es6$promise$$internal$$handleOwnThenable(promise, maybeThenable);
      } else {
        var then = lib$es6$promise$$internal$$getThen(maybeThenable);

        if (then === lib$es6$promise$$internal$$GET_THEN_ERROR) {
          lib$es6$promise$$internal$$reject(promise, lib$es6$promise$$internal$$GET_THEN_ERROR.error);
        } else if (then === undefined) {
          lib$es6$promise$$internal$$fulfill(promise, maybeThenable);
        } else if (lib$es6$promise$utils$$isFunction(then)) {
          lib$es6$promise$$internal$$handleForeignThenable(promise, maybeThenable, then);
        } else {
          lib$es6$promise$$internal$$fulfill(promise, maybeThenable);
        }
      }
    }

    function lib$es6$promise$$internal$$resolve(promise, value) {
      if (promise === value) {
        lib$es6$promise$$internal$$reject(promise, lib$es6$promise$$internal$$selfFullfillment());
      } else if (lib$es6$promise$utils$$objectOrFunction(value)) {
        lib$es6$promise$$internal$$handleMaybeThenable(promise, value);
      } else {
        lib$es6$promise$$internal$$fulfill(promise, value);
      }
    }

    function lib$es6$promise$$internal$$publishRejection(promise) {
      if (promise._onerror) {
        promise._onerror(promise._result);
      }

      lib$es6$promise$$internal$$publish(promise);
    }

    function lib$es6$promise$$internal$$fulfill(promise, value) {
      if (promise._state !== lib$es6$promise$$internal$$PENDING) { return; }

      promise._result = value;
      promise._state = lib$es6$promise$$internal$$FULFILLED;

      if (promise._subscribers.length !== 0) {
        lib$es6$promise$asap$$asap(lib$es6$promise$$internal$$publish, promise);
      }
    }

    function lib$es6$promise$$internal$$reject(promise, reason) {
      if (promise._state !== lib$es6$promise$$internal$$PENDING) { return; }
      promise._state = lib$es6$promise$$internal$$REJECTED;
      promise._result = reason;

      lib$es6$promise$asap$$asap(lib$es6$promise$$internal$$publishRejection, promise);
    }

    function lib$es6$promise$$internal$$subscribe(parent, child, onFulfillment, onRejection) {
      var subscribers = parent._subscribers;
      var length = subscribers.length;

      parent._onerror = null;

      subscribers[length] = child;
      subscribers[length + lib$es6$promise$$internal$$FULFILLED] = onFulfillment;
      subscribers[length + lib$es6$promise$$internal$$REJECTED]  = onRejection;

      if (length === 0 && parent._state) {
        lib$es6$promise$asap$$asap(lib$es6$promise$$internal$$publish, parent);
      }
    }

    function lib$es6$promise$$internal$$publish(promise) {
      var subscribers = promise._subscribers;
      var settled = promise._state;

      if (subscribers.length === 0) { return; }

      var child, callback, detail = promise._result;

      for (var i = 0; i < subscribers.length; i += 3) {
        child = subscribers[i];
        callback = subscribers[i + settled];

        if (child) {
          lib$es6$promise$$internal$$invokeCallback(settled, child, callback, detail);
        } else {
          callback(detail);
        }
      }

      promise._subscribers.length = 0;
    }

    function lib$es6$promise$$internal$$ErrorObject() {
      this.error = null;
    }

    var lib$es6$promise$$internal$$TRY_CATCH_ERROR = new lib$es6$promise$$internal$$ErrorObject();

    function lib$es6$promise$$internal$$tryCatch(callback, detail) {
      try {
        return callback(detail);
      } catch(e) {
        lib$es6$promise$$internal$$TRY_CATCH_ERROR.error = e;
        return lib$es6$promise$$internal$$TRY_CATCH_ERROR;
      }
    }

    function lib$es6$promise$$internal$$invokeCallback(settled, promise, callback, detail) {
      var hasCallback = lib$es6$promise$utils$$isFunction(callback),
          value, error, succeeded, failed;

      if (hasCallback) {
        value = lib$es6$promise$$internal$$tryCatch(callback, detail);

        if (value === lib$es6$promise$$internal$$TRY_CATCH_ERROR) {
          failed = true;
          error = value.error;
          value = null;
        } else {
          succeeded = true;
        }

        if (promise === value) {
          lib$es6$promise$$internal$$reject(promise, lib$es6$promise$$internal$$cannotReturnOwn());
          return;
        }

      } else {
        value = detail;
        succeeded = true;
      }

      if (promise._state !== lib$es6$promise$$internal$$PENDING) {
        // noop
      } else if (hasCallback && succeeded) {
        lib$es6$promise$$internal$$resolve(promise, value);
      } else if (failed) {
        lib$es6$promise$$internal$$reject(promise, error);
      } else if (settled === lib$es6$promise$$internal$$FULFILLED) {
        lib$es6$promise$$internal$$fulfill(promise, value);
      } else if (settled === lib$es6$promise$$internal$$REJECTED) {
        lib$es6$promise$$internal$$reject(promise, value);
      }
    }

    function lib$es6$promise$$internal$$initializePromise(promise, resolver) {
      try {
        resolver(function resolvePromise(value){
          lib$es6$promise$$internal$$resolve(promise, value);
        }, function rejectPromise(reason) {
          lib$es6$promise$$internal$$reject(promise, reason);
        });
      } catch(e) {
        lib$es6$promise$$internal$$reject(promise, e);
      }
    }

    function lib$es6$promise$enumerator$$Enumerator(Constructor, input) {
      var enumerator = this;

      enumerator._instanceConstructor = Constructor;
      enumerator.promise = new Constructor(lib$es6$promise$$internal$$noop);

      if (enumerator._validateInput(input)) {
        enumerator._input     = input;
        enumerator.length     = input.length;
        enumerator._remaining = input.length;

        enumerator._init();

        if (enumerator.length === 0) {
          lib$es6$promise$$internal$$fulfill(enumerator.promise, enumerator._result);
        } else {
          enumerator.length = enumerator.length || 0;
          enumerator._enumerate();
          if (enumerator._remaining === 0) {
            lib$es6$promise$$internal$$fulfill(enumerator.promise, enumerator._result);
          }
        }
      } else {
        lib$es6$promise$$internal$$reject(enumerator.promise, enumerator._validationError());
      }
    }

    lib$es6$promise$enumerator$$Enumerator.prototype._validateInput = function(input) {
      return lib$es6$promise$utils$$isArray(input);
    };

    lib$es6$promise$enumerator$$Enumerator.prototype._validationError = function() {
      return new Error('Array Methods must be provided an Array');
    };

    lib$es6$promise$enumerator$$Enumerator.prototype._init = function() {
      this._result = new Array(this.length);
    };

    var lib$es6$promise$enumerator$$default = lib$es6$promise$enumerator$$Enumerator;

    lib$es6$promise$enumerator$$Enumerator.prototype._enumerate = function() {
      var enumerator = this;

      var length  = enumerator.length;
      var promise = enumerator.promise;
      var input   = enumerator._input;

      for (var i = 0; promise._state === lib$es6$promise$$internal$$PENDING && i < length; i++) {
        enumerator._eachEntry(input[i], i);
      }
    };

    lib$es6$promise$enumerator$$Enumerator.prototype._eachEntry = function(entry, i) {
      var enumerator = this;
      var c = enumerator._instanceConstructor;

      if (lib$es6$promise$utils$$isMaybeThenable(entry)) {
        if (entry.constructor === c && entry._state !== lib$es6$promise$$internal$$PENDING) {
          entry._onerror = null;
          enumerator._settledAt(entry._state, i, entry._result);
        } else {
          enumerator._willSettleAt(c.resolve(entry), i);
        }
      } else {
        enumerator._remaining--;
        enumerator._result[i] = entry;
      }
    };

    lib$es6$promise$enumerator$$Enumerator.prototype._settledAt = function(state, i, value) {
      var enumerator = this;
      var promise = enumerator.promise;

      if (promise._state === lib$es6$promise$$internal$$PENDING) {
        enumerator._remaining--;

        if (state === lib$es6$promise$$internal$$REJECTED) {
          lib$es6$promise$$internal$$reject(promise, value);
        } else {
          enumerator._result[i] = value;
        }
      }

      if (enumerator._remaining === 0) {
        lib$es6$promise$$internal$$fulfill(promise, enumerator._result);
      }
    };

    lib$es6$promise$enumerator$$Enumerator.prototype._willSettleAt = function(promise, i) {
      var enumerator = this;

      lib$es6$promise$$internal$$subscribe(promise, undefined, function(value) {
        enumerator._settledAt(lib$es6$promise$$internal$$FULFILLED, i, value);
      }, function(reason) {
        enumerator._settledAt(lib$es6$promise$$internal$$REJECTED, i, reason);
      });
    };
    function lib$es6$promise$promise$all$$all(entries) {
      return new lib$es6$promise$enumerator$$default(this, entries).promise;
    }
    var lib$es6$promise$promise$all$$default = lib$es6$promise$promise$all$$all;
    function lib$es6$promise$promise$race$$race(entries) {
      /*jshint validthis:true */
      var Constructor = this;

      var promise = new Constructor(lib$es6$promise$$internal$$noop);

      if (!lib$es6$promise$utils$$isArray(entries)) {
        lib$es6$promise$$internal$$reject(promise, new TypeError('You must pass an array to race.'));
        return promise;
      }

      var length = entries.length;

      function onFulfillment(value) {
        lib$es6$promise$$internal$$resolve(promise, value);
      }

      function onRejection(reason) {
        lib$es6$promise$$internal$$reject(promise, reason);
      }

      for (var i = 0; promise._state === lib$es6$promise$$internal$$PENDING && i < length; i++) {
        lib$es6$promise$$internal$$subscribe(Constructor.resolve(entries[i]), undefined, onFulfillment, onRejection);
      }

      return promise;
    }
    var lib$es6$promise$promise$race$$default = lib$es6$promise$promise$race$$race;
    function lib$es6$promise$promise$resolve$$resolve(object) {
      /*jshint validthis:true */
      var Constructor = this;

      if (object && typeof object === 'object' && object.constructor === Constructor) {
        return object;
      }

      var promise = new Constructor(lib$es6$promise$$internal$$noop);
      lib$es6$promise$$internal$$resolve(promise, object);
      return promise;
    }
    var lib$es6$promise$promise$resolve$$default = lib$es6$promise$promise$resolve$$resolve;
    function lib$es6$promise$promise$reject$$reject(reason) {
      /*jshint validthis:true */
      var Constructor = this;
      var promise = new Constructor(lib$es6$promise$$internal$$noop);
      lib$es6$promise$$internal$$reject(promise, reason);
      return promise;
    }
    var lib$es6$promise$promise$reject$$default = lib$es6$promise$promise$reject$$reject;

    var lib$es6$promise$promise$$counter = 0;

    function lib$es6$promise$promise$$needsResolver() {
      throw new TypeError('You must pass a resolver function as the first argument to the promise constructor');
    }

    function lib$es6$promise$promise$$needsNew() {
      throw new TypeError("Failed to construct 'Promise': Please use the 'new' operator, this object constructor cannot be called as a function.");
    }

    var lib$es6$promise$promise$$default = lib$es6$promise$promise$$Promise;
    /**
      Promise objects represent the eventual result of an asynchronous operation. The
      primary way of interacting with a promise is through its `then` method, which
      registers callbacks to receive either a promise's eventual value or the reason
      why the promise cannot be fulfilled.

      Terminology
      -----------

      - `promise` is an object or function with a `then` method whose behavior conforms to this specification.
      - `thenable` is an object or function that defines a `then` method.
      - `value` is any legal JavaScript value (including undefined, a thenable, or a promise).
      - `exception` is a value that is thrown using the throw statement.
      - `reason` is a value that indicates why a promise was rejected.
      - `settled` the final resting state of a promise, fulfilled or rejected.

      A promise can be in one of three states: pending, fulfilled, or rejected.

      Promises that are fulfilled have a fulfillment value and are in the fulfilled
      state.  Promises that are rejected have a rejection reason and are in the
      rejected state.  A fulfillment value is never a thenable.

      Promises can also be said to *resolve* a value.  If this value is also a
      promise, then the original promise's settled state will match the value's
      settled state.  So a promise that *resolves* a promise that rejects will
      itself reject, and a promise that *resolves* a promise that fulfills will
      itself fulfill.


      Basic Usage:
      ------------

      ```js
      var promise = new Promise(function(resolve, reject) {
        // on success
        resolve(value);

        // on failure
        reject(reason);
      });

      promise.then(function(value) {
        // on fulfillment
      }, function(reason) {
        // on rejection
      });
      ```

      Advanced Usage:
      ---------------

      Promises shine when abstracting away asynchronous interactions such as
      `XMLHttpRequest`s.

      ```js
      function getJSON(url) {
        return new Promise(function(resolve, reject){
          var xhr = new XMLHttpRequest();

          xhr.open('GET', url);
          xhr.onreadystatechange = handler;
          xhr.responseType = 'json';
          xhr.setRequestHeader('Accept', 'application/json');
          xhr.send();

          function handler() {
            if (this.readyState === this.DONE) {
              if (this.status === 200) {
                resolve(this.response);
              } else {
                reject(new Error('getJSON: `' + url + '` failed with status: [' + this.status + ']'));
              }
            }
          };
        });
      }

      getJSON('/posts.json').then(function(json) {
        // on fulfillment
      }, function(reason) {
        // on rejection
      });
      ```

      Unlike callbacks, promises are great composable primitives.

      ```js
      Promise.all([
        getJSON('/posts'),
        getJSON('/comments')
      ]).then(function(values){
        values[0] // => postsJSON
        values[1] // => commentsJSON

        return values;
      });
      ```

      @class Promise
      @param {function} resolver
      Useful for tooling.
      @constructor
    */
    function lib$es6$promise$promise$$Promise(resolver) {
      this._id = lib$es6$promise$promise$$counter++;
      this._state = undefined;
      this._result = undefined;
      this._subscribers = [];

      if (lib$es6$promise$$internal$$noop !== resolver) {
        if (!lib$es6$promise$utils$$isFunction(resolver)) {
          lib$es6$promise$promise$$needsResolver();
        }

        if (!(this instanceof lib$es6$promise$promise$$Promise)) {
          lib$es6$promise$promise$$needsNew();
        }

        lib$es6$promise$$internal$$initializePromise(this, resolver);
      }
    }

    lib$es6$promise$promise$$Promise.all = lib$es6$promise$promise$all$$default;
    lib$es6$promise$promise$$Promise.race = lib$es6$promise$promise$race$$default;
    lib$es6$promise$promise$$Promise.resolve = lib$es6$promise$promise$resolve$$default;
    lib$es6$promise$promise$$Promise.reject = lib$es6$promise$promise$reject$$default;
    lib$es6$promise$promise$$Promise._setScheduler = lib$es6$promise$asap$$setScheduler;
    lib$es6$promise$promise$$Promise._setAsap = lib$es6$promise$asap$$setAsap;
    lib$es6$promise$promise$$Promise._asap = lib$es6$promise$asap$$asap;

    lib$es6$promise$promise$$Promise.prototype = {
      constructor: lib$es6$promise$promise$$Promise,

    /**
      The primary way of interacting with a promise is through its `then` method,
      which registers callbacks to receive either a promise's eventual value or the
      reason why the promise cannot be fulfilled.

      ```js
      findUser().then(function(user){
        // user is available
      }, function(reason){
        // user is unavailable, and you are given the reason why
      });
      ```

      Chaining
      --------

      The return value of `then` is itself a promise.  This second, 'downstream'
      promise is resolved with the return value of the first promise's fulfillment
      or rejection handler, or rejected if the handler throws an exception.

      ```js
      findUser().then(function (user) {
        return user.name;
      }, function (reason) {
        return 'default name';
      }).then(function (userName) {
        // If `findUser` fulfilled, `userName` will be the user's name, otherwise it
        // will be `'default name'`
      });

      findUser().then(function (user) {
        throw new Error('Found user, but still unhappy');
      }, function (reason) {
        throw new Error('`findUser` rejected and we're unhappy');
      }).then(function (value) {
        // never reached
      }, function (reason) {
        // if `findUser` fulfilled, `reason` will be 'Found user, but still unhappy'.
        // If `findUser` rejected, `reason` will be '`findUser` rejected and we're unhappy'.
      });
      ```
      If the downstream promise does not specify a rejection handler, rejection reasons will be propagated further downstream.

      ```js
      findUser().then(function (user) {
        throw new PedagogicalException('Upstream error');
      }).then(function (value) {
        // never reached
      }).then(function (value) {
        // never reached
      }, function (reason) {
        // The `PedgagocialException` is propagated all the way down to here
      });
      ```

      Assimilation
      ------------

      Sometimes the value you want to propagate to a downstream promise can only be
      retrieved asynchronously. This can be achieved by returning a promise in the
      fulfillment or rejection handler. The downstream promise will then be pending
      until the returned promise is settled. This is called *assimilation*.

      ```js
      findUser().then(function (user) {
        return findCommentsByAuthor(user);
      }).then(function (comments) {
        // The user's comments are now available
      });
      ```

      If the assimliated promise rejects, then the downstream promise will also reject.

      ```js
      findUser().then(function (user) {
        return findCommentsByAuthor(user);
      }).then(function (comments) {
        // If `findCommentsByAuthor` fulfills, we'll have the value here
      }, function (reason) {
        // If `findCommentsByAuthor` rejects, we'll have the reason here
      });
      ```

      Simple Example
      --------------

      Synchronous Example

      ```javascript
      var result;

      try {
        result = findResult();
        // success
      } catch(reason) {
        // failure
      }
      ```

      Errback Example

      ```js
      findResult(function(result, err){
        if (err) {
          // failure
        } else {
          // success
        }
      });
      ```

      Promise Example;

      ```javascript
      findResult().then(function(result){
        // success
      }, function(reason){
        // failure
      });
      ```

      Advanced Example
      --------------

      Synchronous Example

      ```javascript
      var author, books;

      try {
        author = findAuthor();
        books  = findBooksByAuthor(author);
        // success
      } catch(reason) {
        // failure
      }
      ```

      Errback Example

      ```js

      function foundBooks(books) {

      }

      function failure(reason) {

      }

      findAuthor(function(author, err){
        if (err) {
          failure(err);
          // failure
        } else {
          try {
            findBoooksByAuthor(author, function(books, err) {
              if (err) {
                failure(err);
              } else {
                try {
                  foundBooks(books);
                } catch(reason) {
                  failure(reason);
                }
              }
            });
          } catch(error) {
            failure(err);
          }
          // success
        }
      });
      ```

      Promise Example;

      ```javascript
      findAuthor().
        then(findBooksByAuthor).
        then(function(books){
          // found books
      }).catch(function(reason){
        // something went wrong
      });
      ```

      @method then
      @param {Function} onFulfilled
      @param {Function} onRejected
      Useful for tooling.
      @return {Promise}
    */
      then: function(onFulfillment, onRejection) {
        var parent = this;
        var state = parent._state;

        if (state === lib$es6$promise$$internal$$FULFILLED && !onFulfillment || state === lib$es6$promise$$internal$$REJECTED && !onRejection) {
          return this;
        }

        var child = new this.constructor(lib$es6$promise$$internal$$noop);
        var result = parent._result;

        if (state) {
          var callback = arguments[state - 1];
          lib$es6$promise$asap$$asap(function(){
            lib$es6$promise$$internal$$invokeCallback(state, child, callback, result);
          });
        } else {
          lib$es6$promise$$internal$$subscribe(parent, child, onFulfillment, onRejection);
        }

        return child;
      },

    /**
      `catch` is simply sugar for `then(undefined, onRejection)` which makes it the same
      as the catch block of a try/catch statement.

      ```js
      function findAuthor(){
        throw new Error('couldn't find that author');
      }

      // synchronous
      try {
        findAuthor();
      } catch(reason) {
        // something went wrong
      }

      // async with promises
      findAuthor().catch(function(reason){
        // something went wrong
      });
      ```

      @method catch
      @param {Function} onRejection
      Useful for tooling.
      @return {Promise}
    */
      'catch': function(onRejection) {
        return this.then(null, onRejection);
      }
    };
    function lib$es6$promise$polyfill$$polyfill() {
      var local;

      if (typeof global !== 'undefined') {
          local = global;
      } else if (typeof self !== 'undefined') {
          local = self;
      } else {
          try {
              local = Function('return this')();
          } catch (e) {
              throw new Error('polyfill failed because global object is unavailable in this environment');
          }
      }

      var P = local.Promise;

      // ##### BEGIN: MODIFIED BY SAP
      // Original line:
      //    if (P && Object.prototype.toString.call(P.resolve()) === '[object Promise]' && !P.cast) {
      // This lead to the polyfill replacing the native promise object in
      // - Chrome, where "[object Object]" is returned instead of '[object Promise]'
      // - Safari, where native promise contains a definition for Promise.cast
      if (P && Object.prototype.toString.call(P.resolve()).indexOf('[object ') === 0) {
      // ##### END: MODIFIED BY SAP
        return;
      }

      local.Promise = lib$es6$promise$promise$$default;
    }
    var lib$es6$promise$polyfill$$default = lib$es6$promise$polyfill$$polyfill;

    var lib$es6$promise$umd$$ES6Promise = {
      'Promise': lib$es6$promise$promise$$default,
      'polyfill': lib$es6$promise$polyfill$$default
    };

    /* global define:true module:true window: true */
    if (typeof define === 'function' && define['amd']) {
      // ##### BEGIN: MODIFIED BY SAP
      // Original line:
      // define(function() { return lib$es6$promise$umd$$ES6Promise; });
      define('sap/ui/thirdparty/es6-promise', function() { return lib$es6$promise$umd$$ES6Promise; });
      // ##### END: MODIFIED BY SAP
    } else if (typeof module !== 'undefined' && module['exports']) {
      module['exports'] = lib$es6$promise$umd$$ES6Promise;
      // ##### BEGIN: MODIFIED BY SAP
      // When require.js was loaded before the core, this will not set the global window.ES6Promise property and thus
      // keep the rest of the framework from working in browsers that do not have native Promise support.
      // Original line:
      // } else if (typeof this !== 'undefined') {
    }
    if (typeof this !== 'undefined') {
      // ##### END: MODIFIED BY SAP
      this['ES6Promise'] = lib$es6$promise$umd$$ES6Promise;
    }


    // ##### BEGIN: MODIFIED BY SAP
    // Original line:
    //     lib$es6$promise$polyfill$$default();
    // Do not automatically call the polyfill method as this will be called by UI5 only when needed.
    // ##### END: MODIFIED BY SAP
}).call(this);
/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

/*global ActiveXObject, alert, confirm, console, document, ES6Promise, localStorage, jQuery, performance, URI, Promise, XMLHttpRequest, Proxy */

/**
 * Provides base functionality of the SAP jQuery plugin as extension of the jQuery framework.<br/>
 * See also <a href="http://api.jquery.com/jQuery/">jQuery</a> for details.<br/>
 * Although these functions appear as static ones, they are meant to be used on jQuery instances.<br/>
 * If not stated differently, the functions follow the fluent interface paradigm and return the jQuery instance for chaining of statements.
 *
 * Example for usage of an instance method:
 * <pre>
 *   var oRect = jQuery("#myDiv").rect();
 *   alert("Top Position: " + oRect.top);
 * </pre>
 *
 * @namespace jQuery
 * @public
 */

(function(jQuery, Device, window) {
	"use strict";

	if ( !jQuery ) {
		throw new Error("Loading of jQuery failed");
	}

	// ensure not to initialize twice
	if (jQuery.sap) {
		return;
	}

	// The native Promise in MS Edge and Apple Safari is not fully compliant with the ES6 spec for promises.
	// MS Edge executes callbacks as tasks, not as micro tasks (see https://connect.microsoft.com/IE/feedback/details/1658365).
	// We therefore enforce the use of the es6-promise polyfill also in MS Edge and Safari, which works properly.
	// @see jQuery.sap.promise
	if (Device.browser.edge || Device.browser.safari) {
		window.Promise = undefined; // if not unset, the polyfill assumes that the native Promise is fine
	}

	// Enable promise polyfill if native promise is not available
	if (!window.Promise) {
		ES6Promise.polyfill();
	}

	// early logging support
	var _earlyLogs = [];
	function _earlyLog(sLevel, sMessage) {
		_earlyLogs.push({
			level: sLevel,
			message: sMessage
		});
	}

	var _sBootstrapUrl;

	// -------------------------- VERSION -------------------------------------

	var rVersion = /^[0-9]+(?:\.([0-9]+)(?:\.([0-9]+))?)?(.*)$/;

	/**
	 * Returns a Version instance created from the given parameters.
	 *
	 * This function can either be called as a constructor (using <code>new</code>) or as a normal function.
	 * It always returns an immutable Version instance.
	 *
	 * The parts of the version number (major, minor, patch, suffix) can be provided in several ways:
	 * <ul>
	 * <li>Version("1.2.3-SNAPSHOT")    - as a dot-separated string. Any non-numerical char or a dot followed
	 *                                    by a non-numerical char starts the suffix portion. Any missing major,
	 *                                    minor or patch versions will be set to 0.</li>
	 * <li>Version(1,2,3,"-SNAPSHOT")   - as individual parameters. Major, minor and patch must be integer numbers
	 *                                    or empty, suffix must be a string not starting with digits.</li>
	 * <li>Version([1,2,3,"-SNAPSHOT"]) - as an array with the individual parts. The same type restrictions apply
	 *                                    as before.</li>
	 * <li>Version(otherVersion)        - as a Version instance (cast operation). Returns the given instance instead
	 *                                    of creating a new one.</li>
	 * </ul>
	 *
	 * To keep the code size small, this implementation mainly validates the single string variant.
	 * All other variants are only validated to some degree. It is the responsibility of the caller to
	 * provide proper parts.
	 *
	 * @param {int|string|any[]|jQuery.sap.Version} vMajor the major part of the version (int) or any of the single
	 *        parameter variants explained above.
	 * @param {int} iMinor the minor part of the version number
	 * @param {int} iPatch the patch part of the version number
	 * @param {string} sSuffix the suffix part of the version number
	 * @return {jQuery.sap.Version} the version object as determined from the parameters
	 *
	 * @class Represents a version consisting of major, minor, patch version and suffix, e.g. '1.2.7-SNAPSHOT'.
	 *
	 * @public
	 * @since 1.15.0
	 * @alias jQuery.sap.Version
	 */
	function Version(vMajor, iMinor, iPatch, sSuffix) {
		if ( vMajor instanceof Version ) {
			// note: even a constructor may return a value different from 'this'
			return vMajor;
		}
		if ( !(this instanceof Version) ) {
			// act as a cast operator when called as function (not as a constructor)
			return new Version(vMajor, iMinor, iPatch, sSuffix);
		}

		var m;
		if (typeof vMajor === "string") {
			m = rVersion.exec(vMajor);
		} else if (Array.isArray(vMajor)) {
			m = vMajor;
		} else {
			m = arguments;
		}
		m = m || [];

		function norm(v) {
			v = parseInt(v,10);
			return isNaN(v) ? 0 : v;
		}
		vMajor = norm(m[0]);
		iMinor = norm(m[1]);
		iPatch = norm(m[2]);
		sSuffix = String(m[3] || "");

		/**
		 * Returns a string representation of this version.
		 *
		 * @return {string} a string representation of this version.
		 * @public
		 * @since 1.15.0
		 */
		this.toString = function() {
			return vMajor + "." + iMinor + "." + iPatch + sSuffix;
		};

		/**
		 * Returns the major version part of this version.
		 *
		 * @return {int} the major version part of this version
		 * @public
		 * @since 1.15.0
		 */
		this.getMajor = function() {
			return vMajor;
		};

		/**
		 * Returns the minor version part of this version.
		 *
		 * @return {int} the minor version part of this version
		 * @public
		 * @since 1.15.0
		 */
		this.getMinor = function() {
			return iMinor;
		};

		/**
		 * Returns the patch (or micro) version part of this version.
		 *
		 * @return {int} the patch version part of this version
		 * @public
		 * @since 1.15.0
		 */
		this.getPatch = function() {
			return iPatch;
		};

		/**
		 * Returns the version suffix of this version.
		 *
		 * @return {string} the version suffix of this version
		 * @public
		 * @since 1.15.0
		 */
		this.getSuffix = function() {
			return sSuffix;
		};

		/**
		 * Compares this version with a given one.
		 *
		 * The version with which this version should be compared can be given as a <code>jQuery.sap.Version</code> instance,
		 * as a string (e.g. <code>v.compareto("1.4.5")</code>). Or major, minor, patch and suffix values can be given as
		 * separate parameters (e.g. <code>v.compareTo(1, 4, 5)</code>) or in an array (e.g. <code>v.compareTo([1, 4, 5])</code>).
		 *
		 * @return {int} 0, if the given version is equal to this version, a negative value if the given other version is greater
		 *               and a positive value otherwise
		 * @public
		 * @since 1.15.0
		 */
		this.compareTo = function() {
			var vOther = Version.apply(window, arguments);
			/*eslint-disable no-nested-ternary */
			return vMajor - vOther.getMajor() ||
					iMinor - vOther.getMinor() ||
					iPatch - vOther.getPatch() ||
					((sSuffix < vOther.getSuffix()) ? -1 : (sSuffix === vOther.getSuffix()) ? 0 : 1);
			/*eslint-enable no-nested-ternary */
		};

	}

	/**
	 * Checks whether this version is in the range of the given interval (start inclusive, end exclusive).
	 *
	 * The boundaries against which this version should be checked can be given as  <code>jQuery.sap.Version</code>
	 * instances (e.g. <code>v.inRange(v1, v2)</code>), as strings (e.g. <code>v.inRange("1.4", "2.7")</code>)
	 * or as arrays (e.g. <code>v.inRange([1,4], [2,7])</code>).
	 *
	 * @param {string|any[]|jQuery.sap.Version} vMin the start of the range (inclusive)
	 * @param {string|any[]|jQuery.sap.Version} vMax the end of the range (exclusive)
	 * @return {boolean} <code>true</code> if this version is greater or equal to <code>vMin</code> and smaller
	 *                   than <code>vMax</code>, <code>false</code> otherwise.
	 * @public
	 * @since 1.15.0
	 */
	Version.prototype.inRange = function(vMin, vMax) {
		return this.compareTo(vMin) >= 0 && this.compareTo(vMax) < 0;
	};

	// -----------------------------------------------------------------------

	var oJQVersion = Version(jQuery.fn.jquery);
	if ( oJQVersion.compareTo("2.2.3") != 0 ) {
		// if the loaded jQuery version isn't SAPUI5's default version -> notify
		// the application
		_earlyLog("warning", "SAPUI5's default jQuery version is 2.2.3; current version is " + jQuery.fn.jquery + ". Please note that we only support version 2.2.3.");
	}

	// TODO move to a separate module? Only adds 385 bytes (compressed), but...
	if ( !jQuery.browser ) {
		// re-introduce the jQuery.browser support if missing (jQuery-1.9ff)
		jQuery.browser = (function( ua ) {

			var rwebkit = /(webkit)[ \/]([\w.]+)/,
				ropera = /(opera)(?:.*version)?[ \/]([\w.]+)/,
				rmsie = /(msie) ([\w.]+)/,
				rmozilla = /(mozilla)(?:.*? rv:([\w.]+))?/,
				ua = ua.toLowerCase(),
				match = rwebkit.exec( ua ) ||
					ropera.exec( ua ) ||
					rmsie.exec( ua ) ||
					ua.indexOf("compatible") < 0 && rmozilla.exec( ua ) ||
					[],
				browser = {};

			if ( match[1] ) {
				browser[ match[1] ] = true;
				browser.version = match[2] || "0";
				if ( browser.webkit ) {
					browser.safari = true;
				}
			}

			return browser;

		}(window.navigator.userAgent));
	}

	// XHR overrides for IE
	if ( Device.browser.msie ) {

		// Fixes the CORS issue (introduced by jQuery 1.7) when loading resources
		// (e.g. SAPUI5 script) from other domains for IE browsers.
		// The CORS check in jQuery filters out such browsers who do not have the
		// property "withCredentials" which is the IE and Opera and prevents those
		// browsers to request data from other domains with jQuery.ajax. The CORS
		// requests are simply forbidden nevertheless if it works. In our case we
		// simply load our script resources from another domain when using the CDN
		// variant of SAPUI5. The following fix is also recommended by jQuery:
		jQuery.support = jQuery.support || {};
		jQuery.support.cors = true;

		// Fixes XHR factory issue (introduced by jQuery 1.11). In case of IE
		// it uses by mistake the ActiveXObject XHR. In the list of XHR supported
		// HTTP methods PATCH and MERGE are missing which are required for OData.
		// The related ticket is: #2068 (no downported to jQuery 1.x planned)
		// the fix will only be applied to jQuery >= 1.11.0 (only for jQuery 1.x)
		if ( window.ActiveXObject !== undefined && oJQVersion.inRange("1.11", "2") ) {
			var fnCreateStandardXHR = function() {
				try {
					return new XMLHttpRequest();
				} catch (e) { /* ignore */ }
			};
			var fnCreateActiveXHR = function() {
				try {
					return new ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) { /* ignore */ }
			};
			jQuery.ajaxSettings = jQuery.ajaxSettings || {};
			jQuery.ajaxSettings.xhr = function() {
				return !this.isLocal ? fnCreateStandardXHR() : fnCreateActiveXHR();
			};
		}

	}

	// XHR proxy for Firefox
	if ( Device.browser.firefox && window.Proxy ) {

		// Firefox has an issue with synchronous and asynchronous requests running in parallel,
		// where callbacks of the asynchronous call are executed while waiting on the synchronous
		// response, see https://bugzilla.mozilla.org/show_bug.cgi?id=697151
		// In UI5 in some cases it happens that application code is running, while the class loading
		// is still in process, so classes cannot be found. To overcome this issue we create a proxy
		// of the XHR object, which delays execution of the asynchronous event handlers, until
		// the synchronous request is completed.
		(function() {
			var bSyncRequestOngoing = false,
				bPromisesQueued = false;

			// Overwrite setTimeout and Promise handlers to delay execution after
			// synchronous request is completed
			var _then = Promise.prototype.then,
				_catch = Promise.prototype.catch,
				_timeout = window.setTimeout,
				_interval = window.setInterval,
				aQueue = [];
			function addPromiseHandler(fnHandler) {
				// Collect all promise handlers and execute within the same timeout,
				// to avoid them to be split among several tasks
				if (!bPromisesQueued) {
					bPromisesQueued = true;
					_timeout(function() {
						var aCurrentQueue = aQueue;
						aQueue = [];
						bPromisesQueued = false;
						aCurrentQueue.forEach(function(fnQueuedHandler) {
							fnQueuedHandler();
						});
					}, 0);
				}
				aQueue.push(fnHandler);
			}
			function wrapPromiseHandler(fnHandler, oScope, bCatch) {
				if (typeof fnHandler !== "function") {
					return fnHandler;
				}
				return function() {
					var aArgs = Array.prototype.slice.call(arguments);
					// If a sync request is ongoing or other promises are still queued,
					// the execution needs to be delayed
					if (bSyncRequestOngoing || bPromisesQueued) {
						return new Promise(function(resolve, reject) {
							// The try catch is needed to differentiate whether resolve or
							// reject needs to be called.
							addPromiseHandler(function() {
								var oResult;
								try {
									oResult = fnHandler.apply(window, aArgs);
									resolve(oResult);
								} catch (oException) {
									reject(oException);
								}
							});
						});
					}
					return fnHandler.apply(window, aArgs);
				};
			}
			/*eslint-disable no-extend-native*/
			Promise.prototype.then = function(fnThen, fnCatch) {
				var fnWrappedThen = wrapPromiseHandler(fnThen),
					fnWrappedCatch = wrapPromiseHandler(fnCatch);
				return _then.call(this, fnWrappedThen, fnWrappedCatch);
			};
			Promise.prototype.catch = function(fnCatch) {
				var fnWrappedCatch = wrapPromiseHandler(fnCatch);
				return _catch.call(this, fnWrappedCatch);
			};
			/*eslint-enable no-extend-native*/

			// If there are promise handlers waiting for execution at the time the
			// timeout fires, start another timeout to postpone timer execution after
			// promise execution.
			function wrapTimerHandler(fnHandler) {
				var fnWrappedHandler = function() {
					var aArgs;
					if (bPromisesQueued) {
						aArgs = [fnWrappedHandler, 0].concat(arguments);
						_timeout.apply(window, aArgs);
					} else {
						fnHandler.apply(window, arguments);
					}
				};
				return fnWrappedHandler;
			}
			// setTimeout and setInterval can have arbitrary number of additional
			// parameters, which are passed to the handler function when invoked.
			window.setTimeout = function(vHandler) {
				var aArgs = Array.prototype.slice.call(arguments),
					fnHandler = typeof vHandler === "string" ? new Function(vHandler) : vHandler, // eslint-disable-line no-new-func
					fnWrappedHandler = wrapTimerHandler(fnHandler);
				aArgs[0] = fnWrappedHandler;
				return _timeout.apply(window, aArgs);
			};
			window.setInterval = function(vHandler) {
				var aArgs = Array.prototype.slice.call(arguments),
					fnHandler = typeof vHandler === "string" ? new Function(vHandler) : vHandler, // eslint-disable-line no-new-func
					fnWrappedHandler = wrapTimerHandler(fnHandler, true);
				aArgs[0] = fnWrappedHandler;
				return _interval.apply(window, aArgs);
			};

			// Replace the XMLHttpRequest object with a proxy, that overrides the constructor to
			// return a proxy of the XHR instance
			window.XMLHttpRequest = new Proxy(window.XMLHttpRequest, {
				construct: function(oTargetClass, aArguments, oNewTarget) {
					var oXHR = new oTargetClass(),
						bSync = false,
						bDelay = false,
						iReadyState = 0,
						oProxy;

					// Return a wrapped handler function for the given function, which checks
					// whether a synchronous request is currently in progress.
					function wrapHandler(fnHandler) {
						var fnWrappedHandler = function(oEvent) {
							// The ready state at the time the event is occurring needs to
							// be preserved, to restore it when the handler is called delayed
							var iCurrentState = oXHR.readyState;
							function callHandler() {
								iReadyState = iCurrentState;
								// Only if the event has not been removed in the meantime
								// the handler needs to be called after the timeout
								if (fnWrappedHandler.active) {
									return fnHandler.call(oProxy, oEvent);
								}
							}
							// If this is a asynchronous request and a sync request is ongoing,
							// the execution of all following handler calls needs to be delayed
							if (!bSync && bSyncRequestOngoing) {
								bDelay = true;
							}
							if (bDelay) {
								_timeout(callHandler, 0);
								return true;
							}
							return callHandler();
						};
						fnHandler.wrappedHandler = fnWrappedHandler;
						fnWrappedHandler.active = true;
						return fnWrappedHandler;
					}

					// To be able to remove an event listener, we need to get access to the
					// wrapped handler, which has been used to add the listener internally
					// in the XHR.
					function unwrapHandler(fnHandler) {
						return deactivate(fnHandler.wrappedHandler);
					}

					// When a event handler is removed synchronously, it needs to be deactivated
					// to avoid the situation, where the handler has been triggered while
					// the sync request was ongoing, but removed afterwards.
					function deactivate(fnWrappedHandler) {
						if (typeof fnWrappedHandler === "function") {
							fnWrappedHandler.active = false;
						}
						return fnWrappedHandler;
					}

					// Create a proxy of the XHR instance, which overrides the necessary functions
					// to deal with event handlers and readyState
					oProxy = new Proxy(oXHR, {
						get: function(oTarget, sPropName, oReceiver) {
							var vProp = oTarget[sPropName];
							switch (sPropName) {
								// When an event handler is called with setTimeout, the readyState
								// of the internal XHR is already completed, but we need to have
								// have the readyState at the time the event was fired.
								case "readyState":
									return iReadyState;
								// When events are added, the handler function needs to be wrapped
								case "addEventListener":
									return function(sName, fnHandler, bCapture) {
										vProp.call(oTarget, sName, wrapHandler(fnHandler), bCapture);
									};
								// When events are removed, the wrapped handler function must be used,
								// to remove it on the internal XHR object
								case "removeEventListener":
									return function(sName, fnHandler, bCapture) {
										vProp.call(oTarget, sName, unwrapHandler(fnHandler), bCapture);
									};
								// Whether a request is asynchronous or synchronous is defined when
								// calling the open method.
								case "open":
									return function(sMethod, sUrl, bAsync) {
										bSync = bAsync === false;
										vProp.apply(oTarget, arguments);
										iReadyState = oTarget.readyState;
									};
								// The send method is where the actual request is triggered. For sync
								// requests we set a boolean flag to detect a request is in progress
								// in the wrapped handlers.
								case "send":
									return function() {
										bSyncRequestOngoing = bSync;
										vProp.apply(oTarget, arguments);
										iReadyState = oTarget.readyState;
										bSyncRequestOngoing = false;
									};
							}
							// All functions need to be wrapped, so they are called on the correct object
							// instance
							if (typeof vProp === "function") {
								return function() {
									return vProp.apply(oTarget, arguments);
								};
							}
							// All other properties can just be returned
							return vProp;
						},
						set: function(oTarget, sPropName, vValue) {
							// All properties starting with "on" (event handler functions) need to be wrapped
							// when they are set
							if (sPropName.indexOf("on") === 0) {
								// In case there already is a function set on this property, it needs to be
								// deactivated
								deactivate(oTarget[sPropName]);
								if (typeof vValue === "function") {
									oTarget[sPropName] = wrapHandler(vValue);
									return true;
								}
							}
							// All other properties can just be set on the inner XHR object
							oTarget[sPropName] = vValue;
							return true;
						}
					});
					// add dummy readyStateChange listener to make sure readyState is updated properly
					oProxy.addEventListener("readystatechange", function() {});
					return oProxy;
				}
			});
		})();

	}

	/**
	 * Find the script URL where the SAPUI5 is loaded from and return an object which
	 * contains the identified script-tag and resource root
	 */
	var _oBootstrap = (function() {
		var oTag, sUrl, sResourceRoot,
			reConfigurator = /^(.*\/)?download\/configurator[\/\?]/,
			reBootScripts = /^(.*\/)?(sap-ui-(core|custom|boot|merged)(-.*)?)\.js([?#]|$)/,
			reResources = /^(.*\/)?resources\//;

		// check all script tags that have a src attribute
		jQuery("script[src]").each(function() {
			var src = this.getAttribute("src"),
				m;
			if ( (m = src.match(reConfigurator)) !== null ) {
				// guess 1: script tag src contains "/download/configurator[/?]" (for dynamically created bootstrap files)
				oTag = this;
				sUrl = src;
				sResourceRoot = (m[1] || "") + "resources/";
				return false;
			} else if ( (m = src.match(reBootScripts)) !== null ) {
				// guess 2: src contains one of the well known boot script names
				oTag = this;
				sUrl = src;
				sResourceRoot = m[1] || "";
				return false;
			} else if ( this.id == 'sap-ui-bootstrap' && (m = src.match(reResources)) ) {
				// guess 2: script tag has well known id and src contains "resources/"
				oTag = this;
				sUrl = src;
				sResourceRoot = m[0];
				return false;
			}
		});
		return {
			tag: oTag,
			url: sUrl,
			resourceRoot: sResourceRoot
		};
	})();

	/**
	 * Determine whether sap-bootstrap-debug is set, run debugger statement and allow
	 * to restart the core from a new URL
	 */
	(function() {
		if (/sap-bootstrap-debug=(true|x|X)/.test(location.search)) {
			// Dear developer, the way to reload UI5 from a different location has changed: it can now be directly configured in the support popup (Ctrl-Alt-Shift-P),
			// without stepping into the debugger.
			// However, for convenience or cases where this popup is disabled, or for other usages of an early breakpoint, the "sap-bootstrap-debug" URL parameter option is still available.
			// To reboot an alternative core just step down a few lines and set sRebootUrl
			/*eslint-disable no-debugger */
			debugger;
		}

		// Check local storage for booting a different core
		var sRebootUrl;
		try { // Necessary for FF when Cookies are disabled
			sRebootUrl = window.localStorage.getItem("sap-ui-reboot-URL");
			window.localStorage.removeItem("sap-ui-reboot-URL"); // only reboot once from there (to avoid a deadlock when the alternative core is broken)
		} catch (e) { /* no warning, as this will happen on every startup, depending on browser settings */ }

		if (sRebootUrl && sRebootUrl !== "undefined") { // sic! It can be a string.
			/*eslint-disable no-alert*/
			var bUserConfirmed = confirm("WARNING!\n\nUI5 will be booted from the URL below.\nPress 'Cancel' unless you have configured this.\n\n" + sRebootUrl);
			/*eslint-enable no-alert*/

			if (bUserConfirmed) {
				// replace the bootstrap tag with a newly created script tag to enable restarting the core from a different server
				var oScript = _oBootstrap.tag,
					sScript = "<script src=\"" + sRebootUrl + "\"";
				jQuery.each(oScript.attributes, function(i, oAttr) {
					if (oAttr.nodeName.indexOf("data-sap-ui-") == 0) {
						sScript += " " + oAttr.nodeName + "=\"" + oAttr.nodeValue.replace(/"/g, "&quot;") + "\"";
					}
				});
				sScript += "></script>";
				oScript.parentNode.removeChild(oScript);

				// clean up cachebuster stuff
				jQuery("#sap-ui-bootstrap-cachebusted").remove();
				window["sap-ui-config"] && window["sap-ui-config"].resourceRoots && (window["sap-ui-config"].resourceRoots[""] = undefined);

				document.write(sScript);

				// now this core commits suicide to enable clean loading of the other core
				var oRestart = new Error("This is not a real error. Aborting UI5 bootstrap and rebooting from: " + sRebootUrl);
				oRestart.name = "Restart";
				throw oRestart;
			}
		}
	})();

	/**
	 * Determine whether to use debug sources depending on URL parameter and local storage
	 * and load debug library if necessary
	 */
	(function() {
		// check URI param
		var mUrlMatch = /(?:^|\?|&)sap-ui-debug=([^&]*)(?:&|$)/.exec(location.search),
			vDebugInfo = (mUrlMatch && mUrlMatch[1]) || '';

		// check local storage
		try {
			vDebugInfo = vDebugInfo || window.localStorage.getItem("sap-ui-debug");
		} catch (e) {
			// happens in FF when cookies are deactivated
		}

		// normalize
		if ( /^(?:false|true|x|X)$/.test(vDebugInfo) ) {
			vDebugInfo = vDebugInfo !== 'false';
		}

		window["sap-ui-debug"] = vDebugInfo;

		// if bootstrap URL already contains -dbg URL, just set sap-ui-loaddbg
		if (/-dbg\.js([?#]|$)/.test(_oBootstrap.url)) {
			window["sap-ui-loaddbg"] = true;
			window["sap-ui-debug"] = vDebugInfo = vDebugInfo || true;
		}

		if ( window["sap-ui-optimized"] && vDebugInfo ) {
			// if current sources are optimized and any debug sources should be used, enable the "-dbg" suffix
			window["sap-ui-loaddbg"] = true;
			// if debug sources should be used in general, restart with debug URL
			if ( vDebugInfo === true ) {
				var sDebugUrl = _oBootstrap.url.replace(/\/(?:sap-ui-cachebuster\/)?([^\/]+)\.js/, "/$1-dbg.js");
				window["sap-ui-optimized"] = false;
				document.write("<script type=\"text/javascript\" src=\"" + sDebugUrl + "\"></script>");
				var oRestart = new Error("This is not a real error. Aborting UI5 bootstrap and restarting from: " + sDebugUrl);
				oRestart.name = "Restart";
				throw oRestart;
			}
		}

	})();

	/*
	 * Merged, raw (un-interpreted) configuration data from the following sources
	 * (last one wins)
	 * <ol>
	 * <li>global configuration object <code>window["sap-ui-config"]</code> (could be either a string/url or a configuration object)</li>
	 * <li><code>data-sap-ui-config</code> attribute of the bootstrap script tag</li>
	 * <li>other <code>data-sap-ui-<i>xyz</i></code> attributes of the bootstrap tag</li>
	 * </ol>
	 */
	var oCfgData = window["sap-ui-config"] = (function() {

		function normalize(o) {
			jQuery.each(o, function(i, v) {
				var il = i.toLowerCase();
				if ( !o.hasOwnProperty(il) ) {
					o[il] = v;
					delete o[i];
				}
			});
			return o;
		}

		var oScriptTag = _oBootstrap.tag,
			oCfg = window["sap-ui-config"],
			sCfgFile = "sap-ui-config.json";

		// load the configuration from an external JSON file
		if (typeof oCfg === "string") {
			_earlyLog("warning", "Loading external bootstrap configuration from \"" + oCfg + "\". This is a design time feature and not for productive usage!");
			if (oCfg !== sCfgFile) {
				_earlyLog("warning", "The external bootstrap configuration file should be named \"" + sCfgFile + "\"!");
			}
			jQuery.ajax({
				url : oCfg,
				dataType : 'json',
				async : false,
				success : function(oData, sTextStatus, jqXHR) {
					oCfg = oData;
				},
				error : function(jqXHR, sTextStatus, oError) {
					_earlyLog("error", "Loading externalized bootstrap configuration from \"" + oCfg + "\" failed! Reason: " + oError + "!");
					oCfg = undefined;
				}
			});
			oCfg = oCfg || {};
			oCfg.__loaded = true;
		}

		oCfg = normalize(oCfg || {});
		oCfg.resourceroots = oCfg.resourceroots || {};
		oCfg.themeroots = oCfg.themeroots || {};
		oCfg.resourceroots[''] = oCfg.resourceroots[''] || _oBootstrap.resourceRoot;

		oCfg['xx-loadallmode'] = /(^|\/)(sap-?ui5|[^\/]+-all).js([?#]|$)/.test(_oBootstrap.url);

		// if a script tag has been identified, collect its configuration info
		if ( oScriptTag ) {
			// evaluate the config attribute first - if present
			var sConfig = oScriptTag.getAttribute("data-sap-ui-config");
			if ( sConfig ) {
				try {
					/*eslint-disable no-new-func */
					jQuery.extend(oCfg, normalize((new Function("return {" + sConfig + "};"))())); // TODO jQuery.parseJSON would be better but imposes unwanted restrictions on valid syntax
					/*eslint-enable no-new-func */
				} catch (e) {
					// no log yet, how to report this error?
					_earlyLog("error", "failed to parse data-sap-ui-config attribute: " + (e.message || e));
				}
			}

			// merge with any existing "data-sap-ui-" attributes
			jQuery.each(oScriptTag.attributes, function(i, attr) {
				var m = attr.name.match(/^data-sap-ui-(.*)$/);
				if ( m ) {
					// the following (deactivated) conversion would implement multi-word names like "resource-roots"
					m = m[1].toLowerCase(); // .replace(/\-([a-z])/g, function(s,w) { return w.toUpperCase(); })
					if ( m === 'resourceroots' ) {
						// merge map entries instead of overwriting map
						jQuery.extend(oCfg[m], jQuery.parseJSON(attr.value));
					} else if ( m === 'theme-roots' ) {
						// merge map entries, but rename to camelCase
						jQuery.extend(oCfg.themeroots, jQuery.parseJSON(attr.value));
					} else if ( m !== 'config' ) {
						oCfg[m] = attr.value;
					}
				}
			});
		}

		return oCfg;
	}());

	var syncCallBehavior = 0; // ignore
	if ( oCfgData['xx-nosync'] === 'warn' || /(?:\?|&)sap-ui-xx-nosync=(?:warn)/.exec(window.location.search) ) {
		syncCallBehavior = 1;
	}
	if ( oCfgData['xx-nosync'] === true || oCfgData['xx-nosync'] === 'true' || /(?:\?|&)sap-ui-xx-nosync=(?:x|X|true)/.exec(window.location.search) ) {
		syncCallBehavior = 2;
	}

	if ( syncCallBehavior && oCfgData.__loaded ) {
		_earlyLog(syncCallBehavior === 1 ? "warning" : "error", "[nosync]: configuration loaded via sync XHR");
	}

	// check whether noConflict must be used...
	if ( oCfgData.noconflict === true || oCfgData.noconflict === "true"  || oCfgData.noconflict === "x" ) {
		jQuery.noConflict();
	}

	/**
	 * Root Namespace for the jQuery plug-in provided by SAP SE.
	 *
	 * @version 1.46.7
	 * @namespace
	 * @public
	 * @static
	 */
	jQuery.sap = {};

	// -------------------------- VERSION -------------------------------------

	jQuery.sap.Version = Version;

	// -------------------------- PERFORMANCE NOW -------------------------------------
	/**
	 * Returns a high resolution timestamp for measurements.
	 * The timestamp is based on 01/01/1970 00:00:00 as float with microsecond precision or
	 * with millisecond precision, if high resolution timestamps are not available.
	 * The fractional part of the timestamp represents fractions of a millisecond.
	 * Converting to a <code>Date</code> is possible using <code>new Date(jQuery.sap.now())</code>
	 *
	 * @returns {float} high resolution timestamp for measurements
	 * @public
	 */
	jQuery.sap.now = !(window.performance && performance.now && performance.timing) ? Date.now : (function() {
		var iNavigationStart = performance.timing.navigationStart;
		return function perfnow() {
			return iNavigationStart + performance.now();
		};
	}());

	// -------------------------- supportability helpers that use localStorage -------------------------------------

	// Reads the value for the given key from the localStorage or writes a new value to it.
	function makeLocalStorageAccessor(key, type, callback) {
		return function(value) {
			try {
				if ( value != null || type === 'string' ) {
					if (value) {
						localStorage.setItem(key, type === 'boolean' ? 'X' : value);
					} else {
						localStorage.removeItem(key);
					}
					callback(value);
				}
				value = localStorage.getItem(key);
				return type === 'boolean' ? value === 'X' : value;
			} catch (e) {
				jQuery.sap.log.warning("Could not access localStorage while accessing '" + key + "' (value: '" + value + "', are cookies disabled?): " + e.message);
			}
		};
	}

	jQuery.sap.debug = makeLocalStorageAccessor('sap-ui-debug', '', function reloadHint(vDebugInfo) {
		/*eslint-disable no-alert */
		alert("Usage of debug sources is " + (vDebugInfo ? "on" : "off") + " now.\nFor the change to take effect, you need to reload the page.");
		/*eslint-enable no-alert */
	});

	/**
	 * Sets the URL to reboot this app from, the next time it is started. Only works with localStorage API available
	 * (and depending on the browser, if cookies are enabled, even though cookies are not used).
	 *
	 * @param sRebootUrl the URL to sap-ui-core.js, from which the application should load UI5 on next restart; undefined clears the restart URL
	 * @returns the current reboot URL or undefined in case of an error or when the reboot URL has been cleared
	 *
	 * @private
	 */
	jQuery.sap.setReboot = makeLocalStorageAccessor('sap-ui-reboot-URL', 'string', function rebootUrlHint(sRebootUrl) { // null-ish clears the reboot request
		if ( sRebootUrl ) {
			/*eslint-disable no-alert */
			alert("Next time this app is launched (only once), it will load UI5 from:\n" + sRebootUrl + ".\nPlease reload the application page now.");
			/*eslint-enable no-alert */
		}
	});

	jQuery.sap.statistics = makeLocalStorageAccessor('sap-ui-statistics', 'boolean', function gatewayStatsHint(bUseStatistics) {
		/*eslint-disable no-alert */
		alert("Usage of Gateway statistics " + (bUseStatistics ? "on" : "off") + " now.\nFor the change to take effect, you need to reload the page.");
		/*eslint-enable no-alert */
	});

	// -------------------------- Logging -------------------------------------

	(function() {

		var FATAL = 0, ERROR = 1, WARNING = 2, INFO = 3, DEBUG = 4, TRACE = 5,

		/**
		 * Unique prefix for this instance of the core in a multi-frame environment.
		 */
			sWindowName = (window.top == window) ? "" : "[" + window.location.pathname.split('/').slice(-1)[0] + "] ",
		// Note: comparison must use type coercion (==, not ===), otherwise test fails in IE

		/**
		 * The array that holds the log entries that have been recorded so far
		 */
			aLog = [],

		/**
		 * Maximum log level to be recorded (per component).
		 */
			mMaxLevel = { '' : ERROR },

		/**
		 * Registered listener to be informed about new log entries.
		 */
			oListener = null,

		/**
		 * Additional support information delivered by callback should be logged
		 */
			bLogSupportInfo = false;

		function pad0(i,w) {
			return ("000" + String(i)).slice(-w);
		}

		function level(sComponent) {
			return (!sComponent || isNaN(mMaxLevel[sComponent])) ? mMaxLevel[''] : mMaxLevel[sComponent];
		}

		function listener(){
			if (!oListener) {
				oListener = {
					listeners: [],
					onLogEntry: function(oLogEntry){
						for (var i = 0; i < oListener.listeners.length; i++) {
							if (oListener.listeners[i].onLogEntry) {
								oListener.listeners[i].onLogEntry(oLogEntry);
							}
						}
					},
					attach: function(oLogger, oLstnr){
						if (oLstnr) {
							oListener.listeners.push(oLstnr);
							if (oLstnr.onAttachToLog) {
								oLstnr.onAttachToLog(oLogger);
							}
						}
					},
					detach: function(oLogger, oLstnr){
						for (var i = 0; i < oListener.listeners.length; i++) {
							if (oListener.listeners[i] === oLstnr) {
								if (oLstnr.onDetachFromLog) {
									oLstnr.onDetachFromLog(oLogger);
								}
								oListener.listeners.splice(i,1);
								return;
							}
						}
					}
				};
			}
			return oListener;
		}

		/**
		 * Creates a new log entry depending on its level and component.
		 *
		 * If the given level is higher than the max level for the given component
		 * (or higher than the global level, if no component is given),
		 * then no entry is created and <code>undefined</code> is returned.
		 *
		 * @param {jQuery.sap.log.Level} iLevel One of the log levels FATAL, ERROR, WARNING, INFO, DEBUG, TRACE
		 * @param {string} sMessage The message to be logged
		 * @param {string} [sDetails] The optional details for the message
		 * @param {string} [sComponent] The log component under which the message should be logged
		 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
		 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
		 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
		 *   immutable JSON object with mostly static and stable content.
		 * @returns {object} The log entry as an object or <code>undefined</code> if no entry was created
		 * @private
		 */
		function log(iLevel, sMessage, sDetails, sComponent, fnSupportInfo) {
			if (iLevel <= level(sComponent) ) {
				if (bLogSupportInfo) {
					if (!fnSupportInfo && !sComponent && typeof sDetails === "function") {
						fnSupportInfo = sDetails;
						sDetails = "";
					}
					if (!fnSupportInfo && typeof sComponent === "function") {
						fnSupportInfo = sComponent;
						sComponent = "";
					}
				}
				var fNow =  jQuery.sap.now(),
					oNow = new Date(fNow),
					iMicroSeconds = Math.floor((fNow - Math.floor(fNow)) * 1000),
					oLogEntry = {
						time     : pad0(oNow.getHours(),2) + ":" + pad0(oNow.getMinutes(),2) + ":" + pad0(oNow.getSeconds(),2) + "." + pad0(oNow.getMilliseconds(),3) + pad0(iMicroSeconds,3),
						date     : pad0(oNow.getFullYear(),4) + "-" + pad0(oNow.getMonth() + 1,2) + "-" + pad0(oNow.getDate(),2),
						timestamp: fNow,
						level    : iLevel,
						message  : String(sMessage || ""),
						details  : String(sDetails || ""),
						component: String(sComponent || "")
					};
				if (bLogSupportInfo && typeof fnSupportInfo === "function") {
					oLogEntry.supportInfo = fnSupportInfo();
				}
				aLog.push( oLogEntry );
				if (oListener) {
					oListener.onLogEntry(oLogEntry);
				}

				/*
				 * Console Log, also tries to log to the window.console, if available.
				 *
				 * Unfortunately, the support for window.console is quite different between the UI5 browsers. The most important differences are:
				 * - in IE (checked until IE9), the console object does not exist in a window, until the developer tools are opened for that window.
				 *   After opening the dev tools, the console remains available even when the tools are closed again. Only using a new window (or tab)
				 *   restores the old state without console.
				 *   When the console is available, it provides most standard methods, but not debug and trace
				 * - in FF3.6 the console is not available, until FireBug is opened. It disappears again, when fire bug is closed.
				 *   But when the settings for a web site are stored (convenience), the console remains open
				 *   When the console is available, it supports all relevant methods
				 * - in FF9.0, the console is always available, but method assert is only available when firebug is open
				 * - in Webkit browsers, the console object is always available and has all required methods
				 *   - Exception: in the iOS Simulator, console.info() does not exist
				 */
				/*eslint-disable no-console */
				if (window.console) { // in IE and FF, console might not exist; in FF it might even disappear
					var logText = oLogEntry.date + " " + oLogEntry.time + " " + sWindowName + oLogEntry.message + " - " + oLogEntry.details + " " + oLogEntry.component;
					switch (iLevel) {
					case FATAL:
					case ERROR: console.error(logText); break;
					case WARNING: console.warn(logText); break;
					case INFO: console.info ? console.info(logText) : console.log(logText); break;    // info not available in iOS simulator
					case DEBUG: console.debug ? console.debug(logText) : console.log(logText); break; // debug not available in IE, fallback to log
					case TRACE: console.trace ? console.trace(logText) : console.log(logText); break; // trace not available in IE, fallback to log (no trace)
					// no default
					}
					if (console.info && oLogEntry.supportInfo) {
						console.info(oLogEntry.supportInfo);
					}
				}
				/*eslint-enable no-console */
				return oLogEntry;
			}
		}

		/**
		 * Creates a new Logger instance which will use the given component string
		 * for all logged messages without a specific component.
		 *
		 * @param {string} sDefaultComponent The component to use
		 *
		 * @class A Logger class
		 * @alias jQuery.sap.log.Logger
		 * @since 1.1.2
		 * @public
		 */
		function Logger(sDefaultComponent) {

			/**
			 * Creates a new fatal-level entry in the log with the given message, details and calling component.
			 *
			 * @param {string} sMessage Message text to display
			 * @param {string} [sDetails=''] Details about the message, might be omitted
			 * @param {string} [sComponent=''] Name of the component that produced the log entry
			 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
			 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
			 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
			 *   immutable JSON object with mostly static and stable content.
			 * @return {jQuery.sap.log.Logger} The log instance for method chaining
			 * @public
			 * @SecSink {0 1 2|SECRET} Could expose secret data in logs
			 */
			this.fatal = function (sMessage, sDetails, sComponent, fnSupportInfo) {
				log(FATAL, sMessage, sDetails, sComponent || sDefaultComponent, fnSupportInfo);
				return this;
			};

			/**
			 * Creates a new error-level entry in the log with the given message, details and calling component.
			 *
			 * @param {string} sMessage Message text to display
			 * @param {string} [sDetails=''] Details about the message, might be omitted
			 * @param {string} [sComponent=''] Name of the component that produced the log entry
			 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
			 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
			 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
			 *   immutable JSON object with mostly static and stable content.
			 * @return {jQuery.sap.log.Logger} The log instance
			 * @public
			 * @SecSink {0 1 2|SECRET} Could expose secret data in logs
			 */
			this.error = function error(sMessage, sDetails, sComponent, fnSupportInfo) {
				log(ERROR, sMessage, sDetails, sComponent || sDefaultComponent, fnSupportInfo);
				return this;
			};

			/**
			 * Creates a new warning-level entry in the log with the given message, details and calling component.
			 *
			 * @param {string} sMessage Message text to display
			 * @param {string} [sDetails=''] Details about the message, might be omitted
			 * @param {string} [sComponent=''] Name of the component that produced the log entry
			 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
			 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
			 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
			 *   immutable JSON object with mostly static and stable content.
			 * @return {jQuery.sap.log.Logger} The log instance
			 * @public
			 * @SecSink {0 1 2|SECRET} Could expose secret data in logs
			 */
			this.warning = function warning(sMessage, sDetails, sComponent, fnSupportInfo) {
				log(WARNING, sMessage, sDetails, sComponent || sDefaultComponent, fnSupportInfo);
				return this;
			};

			/**
			 * Creates a new info-level entry in the log with the given message, details and calling component.
			 *
			 * @param {string} sMessage Message text to display
			 * @param {string} [sDetails=''] Details about the message, might be omitted
			 * @param {string} [sComponent=''] Name of the component that produced the log entry
			 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
			 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
			 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
			 *   immutable JSON object with mostly static and stable content.
			 * @return {jQuery.sap.log.Logger} The log instance
			 * @public
			 * @SecSink {0 1 2|SECRET} Could expose secret data in logs
			 */
			this.info = function info(sMessage, sDetails, sComponent, fnSupportInfo) {
				log(INFO, sMessage, sDetails, sComponent || sDefaultComponent, fnSupportInfo);
				return this;
			};
			/**
			 * Creates a new debug-level entry in the log with the given message, details and calling component.
			 *
			 * @param {string} sMessage Message text to display
			 * @param {string} [sDetails=''] Details about the message, might be omitted
			 * @param {string} [sComponent=''] Name of the component that produced the log entry
			 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
			 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
			 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
			 *   immutable JSON object with mostly static and stable content.
			 * @return {jQuery.sap.log.Logger} The log instance
			 * @public
			 * @SecSink {0 1 2|SECRET} Could expose secret data in logs
			 */
			this.debug = function debug(sMessage, sDetails, sComponent, fnSupportInfo) {
				log(DEBUG, sMessage, sDetails, sComponent || sDefaultComponent, fnSupportInfo);
				return this;
			};

			/**
			 * Creates a new trace-level entry in the log with the given message, details and calling component.
			 *
			 * @param {string} sMessage Message text to display
			 * @param {string} [sDetails=''] Details about the message, might be omitted
			 * @param {string} [sComponent=''] Name of the component that produced the log entry
			 * @param {function} [fnSupportInfo] Callback that returns an additional support object to be logged in support mode.
			 *   This function is only called if support info mode is turned on with <code>logSupportInfo(true)</code>.
			 *   To avoid negative effects regarding execution times and memory consumption, the returned object should be a simple
			 *   immutable JSON object with mostly static and stable content.
			 * @return {jQuery.sap.log.Logger} The log-instance
			 * @public
			 * @SecSink {0 1 2|SECRET} Could expose secret data in logs
			 */
			this.trace = function trace(sMessage, sDetails, sComponent, fnSupportInfo) {
				log(TRACE, sMessage, sDetails, sComponent || sDefaultComponent, fnSupportInfo);
				return this;
			};

			/**
			 * Defines the maximum <code>jQuery.sap.log.Level</code> of log entries that will be recorded.
			 * Log entries with a higher (less important) log level will be omitted from the log.
			 * When a component name is given, the log level will be configured for that component
			 * only, otherwise the log level for the default component of this logger is set.
			 * For the global logger, the global default level is set.
			 *
			 * <b>Note</b>: Setting a global default log level has no impact on already defined
			 * component log levels. They always override the global default log level.
			 *
			 * @param {jQuery.sap.log.Level} iLogLevel The new log level
			 * @param {string} [sComponent] The log component to set the log level for
			 * @return {jQuery.sap.log.Logger} This logger object to allow method chaining
			 * @public
			 */
			this.setLevel = function setLevel(iLogLevel, sComponent) {
				sComponent = sComponent || sDefaultComponent || '';
				mMaxLevel[sComponent] = iLogLevel;
				var mBackMapping = [];
				jQuery.each(jQuery.sap.log.LogLevel, function(idx, v){
					mBackMapping[v] = idx;
				});
				log(INFO, "Changing log level " + (sComponent ? "for '" + sComponent + "' " : "") + "to " + mBackMapping[iLogLevel], "", "jQuery.sap.log");
				return this;
			};

			/**
			 * Returns the log level currently effective for the given component.
			 * If no component is given or when no level has been configured for a
			 * given component, the log level for the default component of this logger is returned.
			 *
			 * @param {string} [sComponent] Name of the component to retrieve the log level for
			 * @return {int} The log level for the given component or the default log level
			 * @public
			 * @since 1.1.2
			 */
			this.getLevel = function getLevel(sComponent) {
				return level(sComponent || sDefaultComponent);
			};

			/**
			 * Checks whether logging is enabled for the given log level,
			 * depending on the currently effective log level for the given component.
			 *
			 * If no component is given, the default component of this logger will be taken into account.
			 *
			 * @param {int} [iLevel=Level.DEBUG] The log level in question
			 * @param {string} [sComponent] Name of the component to check the log level for
			 * @return {boolean} Whether logging is enabled or not
			 * @public
			 * @since 1.13.2
			 */
			this.isLoggable = function (iLevel, sComponent) {
				return (iLevel == null ? DEBUG : iLevel) <= level(sComponent || sDefaultComponent);
			};

			/**
			 * Enables or disables whether additional support information is logged in a trace.
			 * If enabled, logging methods like error, warning, info and debug are calling the additional
			 * optional callback parameter fnSupportInfo and store the returned object in the log entry property supportInfo.
			 *
			 * @param {boolean} bEnabled true if the support information should be logged
			 * @private
			 * @since 1.46.0
			 */
			this.logSupportInfo = function logSupportInfo(bEnabled) {
				bLogSupportInfo = bEnabled;
			};
		}

		/**
		 * A Logging API for JavaScript.
		 *
		 * Provides methods to manage a client-side log and to create entries in it. Each of the logging methods
		 * {@link jQuery.sap.log.debug}, {@link jQuery.sap.log.info}, {@link jQuery.sap.log.warning},
		 * {@link jQuery.sap.log.error} and {@link jQuery.sap.log.fatal} creates and records a log entry,
		 * containing a timestamp, a log level, a message with details and a component info.
		 * The log level will be one of {@link jQuery.sap.log.Level} and equals the name of the concrete logging method.
		 *
		 * By using the {@link jQuery.sap.log.setLevel} method, consumers can determine the least important
		 * log level which should be recorded. Less important entries will be filtered out. (Note that higher numeric
		 * values represent less important levels). The initially set level depends on the mode that UI5 is running in.
		 * When the optimized sources are executed, the default level will be {@link jQuery.sap.log.Level.ERROR}.
		 * For normal (debug sources), the default level is {@link jQuery.sap.log.Level.DEBUG}.
		 *
		 * All logging methods allow to specify a <b>component</b>. These components are simple strings and
		 * don't have a special meaning to the UI5 framework. However they can be used to semantically group
		 * log entries that belong to the same software component (or feature). There are two APIs that help
		 * to manage logging for such a component. With <code>{@link jQuery.sap.log.getLogger}(sComponent)</code>,
		 * one can retrieve a logger that automatically adds the given <code>sComponent</code> as component
		 * parameter to each log entry, if no other component is specified. Typically, JavaScript code will
		 * retrieve such a logger once during startup and reuse it for the rest of its lifecycle.
		 * Second, the {@link jQuery.sap.log.Logger#setLevel}(iLevel, sComponent) method allows to set the log level
		 * for a specific component only. This allows a more fine granular control about the created logging entries.
		 * {@link jQuery.sap.log.Logger#getLevel} allows to retrieve the currently effective log level for a given
		 * component.
		 *
		 * {@link jQuery.sap.log.getLogEntries} returns an array of the currently collected log entries.
		 *
		 * Furthermore, a listener can be registered to the log. It will be notified whenever a new entry
		 * is added to the log. The listener can be used for displaying log entries in a separate page area,
		 * or for sending it to some external target (server).
		 *
		 * @since 0.9.0
		 * @namespace
		 * @public
		 * @borrows jQuery.sap.log.Logger#fatal as fatal
		 * @borrows jQuery.sap.log.Logger#error as error
		 * @borrows jQuery.sap.log.Logger#warning as warning
		 * @borrows jQuery.sap.log.Logger#info as info
		 * @borrows jQuery.sap.log.Logger#debug as debug
		 * @borrows jQuery.sap.log.Logger#trace as trace
		 * @borrows jQuery.sap.log.Logger#getLevel as getLevel
		 * @borrows jQuery.sap.log.Logger#setLevel as setLevel
		 * @borrows jQuery.sap.log.Logger#isLoggable as isLoggable
		 */
		jQuery.sap.log = jQuery.extend(new Logger(), /** @lends jQuery.sap.log */ {

			/**
			 * Enumeration of the configurable log levels that a Logger should persist to the log.
			 *
			 * Only if the current LogLevel is higher than the level {@link jQuery.sap.log.Level} of the currently added log entry,
			 * then this very entry is permanently added to the log. Otherwise it is ignored.
			 * @see jQuery.sap.log.Logger#setLevel
			 * @enum {int}
			 * @public
			 */
			Level : {

				/**
				 * Do not log anything
				 * @public
				 */
				NONE : FATAL - 1,

				/**
				 * Fatal level. Use this for logging unrecoverable situations
				 * @public
				 */
				FATAL : FATAL,

				/**
				 * Error level. Use this for logging of erroneous but still recoverable situations
				 * @public
				 */
				ERROR : ERROR,

				/**
				 * Warning level. Use this for logging unwanted but foreseen situations
				 * @public
				 */
				WARNING : WARNING,

				/**
				 * Info level. Use this for logging information of purely informative nature
				 * @public
				 */
				INFO : INFO,

				/**
				 * Debug level. Use this for logging information necessary for debugging
				 * @public
				 */
				DEBUG : DEBUG,

				/**
				 * Trace level. Use this for tracing the program flow.
				 * @public
				 */
				TRACE : TRACE,

				/**
				 * Trace level to log everything.
				 */
				ALL : (TRACE + 1)
			},

			/**
			 * Returns a {@link jQuery.sap.log.Logger} for the given component.
			 *
			 * The method might or might not return the same logger object across multiple calls.
			 * While loggers are assumed to be light weight objects, consumers should try to
			 * avoid redundant calls and instead keep references to already retrieved loggers.
			 *
			 * The optional second parameter <code>iDefaultLogLevel</code> allows to specify
			 * a default log level for the component. It is only applied when no log level has been
			 * defined so far for that component (ignoring inherited log levels). If this method is
			 * called multiple times for the same component but with different log levels,
			 * only the first call one might be taken into account.
			 *
			 * @param {string} sComponent Component to create the logger for
			 * @param {int} [iDefaultLogLevel] a default log level to be used for the component,
			 *   if no log level has been defined for it so far.
			 * @return {jQuery.sap.log.Logger} A logger for the component.
			 * @public
			 * @static
			 * @since 1.1.2
			 */
			getLogger : function(sComponent, iDefaultLogLevel) {
				if ( !isNaN(iDefaultLogLevel) && mMaxLevel[sComponent] == null ) {
					mMaxLevel[sComponent] = iDefaultLogLevel;
				}
				return new Logger(sComponent);
			},

			/**
			 * Returns the logged entries recorded so far as an array.
			 *
			 * Log entries are plain JavaScript objects with the following properties
			 * <ul>
			 * <li>timestamp {number} point in time when the entry was created
			 * <li>level {int} LogLevel level of the entry
			 * <li>message {string} message text of the entry
			 * </ul>
			 *
			 * @return {object[]} an array containing the recorded log entries
			 * @public
			 * @static
			 * @since 1.1.2
			 */
			getLogEntries : function () {
				return aLog.slice();
			},

			/**
			 * Allows to add a new LogListener that will be notified for new log entries.
			 *
			 * The given object must provide method <code>onLogEntry</code> and can also be informed
			 * about <code>onDetachFromLog</code> and <code>onAttachToLog</code>
			 * @param {object} oListener The new listener object that should be informed
			 * @return {jQuery.sap.log} The global logger
			 * @public
			 * @static
			 */
			addLogListener : function(oListener) {
				listener().attach(this, oListener);
				return this;
			},

			/**
			 * Allows to remove a registered LogListener.
			 * @param {object} oListener The new listener object that should be removed
			 * @return {jQuery.sap.log} The global logger
			 * @public
			 * @static
			 */
			removeLogListener : function(oListener) {
				listener().detach(this, oListener);
				return this;
			}

		});

		/**
		 * Enumeration of levels that can be used in a call to {@link jQuery.sap.log.Logger#setLevel}(iLevel, sComponent).
		 *
		 * @deprecated Since 1.1.2. To streamline the Logging API a bit, the separation between Level and LogLevel has been given up.
		 * Use the (enriched) enumeration {@link jQuery.sap.log.Level} instead.
		 * @namespace
		 * @public
		 */
		jQuery.sap.log.LogLevel = jQuery.sap.log.Level;

		/**
		 * Retrieves the currently recorded log entries.
		 * @deprecated Since 1.1.2. To avoid confusion with getLogger, this method has been renamed to {@link jQuery.sap.log.getLogEntries}.
		 * @function
		 * @public
		 */
		jQuery.sap.log.getLog = jQuery.sap.log.getLogEntries;

		/**
		 * A simple assertion mechanism that logs a message when a given condition is not met.
		 *
		 * <b>Note:</b> Calls to this method might be removed when the JavaScript code
		 *              is optimized during build. Therefore, callers should not rely on any side effects
		 *              of this method.
		 *
		 * @param {boolean} bResult Result of the checked assertion
		 * @param {string|function} vMessage Message that will be logged when the result is <code>false</code>. In case this is a function, the return value of the function will be displayed. This can be used to execute complex code only if the assertion fails.
		 *
		 * @public
		 * @static
		 * @SecSink {1|SECRET} Could expose secret data in logs
		 */
		jQuery.sap.assert = function(bResult, vMessage) {
			if ( !bResult ) {
				var sMessage = typeof vMessage === "function" ? vMessage() : vMessage;
				/*eslint-disable no-console */
				if ( window.console && console.assert ) {
					console.assert(bResult, sWindowName + sMessage);
				} else {
					// console is not always available (IE, FF) and IE doesn't support console.assert
					jQuery.sap.log.debug("[Assertions] " + sMessage);
				}
				/*eslint-enable no-console */
			}
		};

		// against all our rules: use side effect of assert to differentiate between optimized and productive code
		jQuery.sap.assert( !!(mMaxLevel[''] = DEBUG), "will be removed in optimized version");

		// evaluate configuration
		oCfgData.loglevel = (function() {
			var m = /(?:\?|&)sap-ui-log(?:L|-l)evel=([^&]*)/.exec(window.location.search);
			return m && m[1];
		}()) || oCfgData.loglevel;
		if ( oCfgData.loglevel ) {
			jQuery.sap.log.setLevel(jQuery.sap.log.Level[oCfgData.loglevel.toUpperCase()] || parseInt(oCfgData.loglevel,10));
		}

		jQuery.sap.log.info("SAP Logger started.");
		// log early logs
		jQuery.each(_earlyLogs, function(i,e) {
			jQuery.sap.log[e.level](e.message);
		});
		_earlyLogs = null;

	}());

	// ---------------------------------------------------------------------------------------------------

	/**
	 * Returns a new constructor function that creates objects with
	 * the given prototype.
	 *
	 * As of 1.45.0, this method has been deprecated. Use the following code pattern instead:
	 * <pre>
	 *   function MyFunction() {
	 *   };
	 *   MyFunction.prototype = oPrototype;
	 * </pre>
	 * @param {object} oPrototype Prototype to use for the new objects
	 * @return {function} the newly created constructor function
	 * @public
	 * @static
	 * @deprecated As of 1.45.0, define your own function and assign <code>oPrototype</code> to its <code>prototype</code> property instead.
	 */
	jQuery.sap.factory = function factory(oPrototype) {
		jQuery.sap.assert(typeof oPrototype == "object", "oPrototype must be an object (incl. null)");
		function Factory() {}
		Factory.prototype = oPrototype;
		return Factory;
	};

	/**
	 * Returns a new object which has the given <code>oPrototype</code> as its prototype.
	 *
	 * If several objects with the same prototype are to be created,
	 * {@link jQuery.sap.factory} should be used instead.
	 *
	 * @param {object} oPrototype Prototype to use for the new object
	 * @return {object} new object
	 * @public
	 * @static
	 * @deprecated As of 1.45.0, use <code>Object.create(oPrototype)</code> instead.
	 */
	jQuery.sap.newObject = function newObject(oPrototype) {
		jQuery.sap.assert(typeof oPrototype == "object", "oPrototype must be an object (incl. null)");
		// explicitly fall back to null for best compatibility with old implementation
		return Object.create(oPrototype || null);
	};

	/**
	 * Returns a new function that returns the given <code>oValue</code> (using its closure).
	 *
	 * Avoids the need for a dedicated member for the value.
	 *
	 * As closures don't come for free, this function should only be used when polluting
	 * the enclosing object is an absolute "must-not" (as it is the case in public base classes).
	 *
	 * @param {object} oValue The value that the getter should return
	 * @returns {function} The new getter function
	 * @public
	 * @static
	 */
	jQuery.sap.getter = function getter(oValue) {
		return function() {
			return oValue;
		};
	};

	/**
	 * Returns a JavaScript object which is identified by a sequence of names.
	 *
	 * A call to <code>getObject("a.b.C")</code> has essentially the same effect
	 * as accessing <code>window.a.b.C</code> but with the difference that missing
	 * intermediate objects (a or b in the example above) don't lead to an exception.
	 *
	 * When the addressed object exists, it is simply returned. If it doesn't exists,
	 * the behavior depends on the value of the second, optional parameter
	 * <code>iNoCreates</code> (assuming 'n' to be the number of names in the name sequence):
	 * <ul>
	 * <li>NaN: if iNoCreates is not a number and the addressed object doesn't exist,
	 *          then <code>getObject()</code> returns <code>undefined</code>.
	 * <li>0 &lt; iNoCreates &lt; n: any non-existing intermediate object is created, except
	 *          the <i>last</i> <code>iNoCreates</code> ones.
	 * </ul>
	 *
	 * Example:
	 * <pre>
	 *   getObject()            -- returns the context object (either param or window)
	 *   getObject("a.b.C")     -- will only try to get a.b.C and return undefined if not found.
	 *   getObject("a.b.C", 0)  -- will create a, b, and C in that order if they don't exists
	 *   getObject("a.b.c", 1)  -- will create a and b, but not C.
	 * </pre>
	 *
	 * When a <code>oContext</code> is given, the search starts in that object.
	 * Otherwise it starts in the <code>window</code> object that this plugin
	 * has been created in.
	 *
	 * Note: Although this method internally uses <code>object["key"]</code> to address object
	 *       properties, it does not support all possible characters in a name.
	 *       Especially the dot ('.') is not supported in the individual name segments,
	 *       as it is always interpreted as a name separator.
	 *
	 * @param {string} sName  a dot separated sequence of names that identify the required object
	 * @param {int}    [iNoCreates=NaN] number of objects (from the right) that should not be created
	 * @param {object} [oContext=window] the context to execute the search in
	 * @returns {function} The value of the named object
	 *
	 * @public
	 * @static
	 */
	jQuery.sap.getObject = function getObject(sName, iNoCreates, oContext) {
		var oObject = oContext || window,
			aNames = (sName || "").split("."),
			l = aNames.length,
			iEndCreate = isNaN(iNoCreates) ? 0 : l - iNoCreates,
			i;

		if ( syncCallBehavior && oContext === window ) {
			jQuery.sap.log.error("[nosync] getObject called to retrieve global name '" + sName + "'");
		}

		for (i = 0; oObject && i < l; i++) {
			if (!oObject[aNames[i]] && i < iEndCreate ) {
				oObject[aNames[i]] = {};
			}
			oObject = oObject[aNames[i]];
		}
		return oObject;

	};

	/**
	 * Sets an object property to a given value, where the property is
	 * identified by a sequence of names (path).
	 *
	 * When a <code>oContext</code> is given, the path starts in that object.
	 * Otherwise it starts in the <code>window</code> object that this plugin
	 * has been created for.
	 *
	 * Note: Although this method internally uses <code>object["key"]</code> to address object
	 *       properties, it does not support all possible characters in a name.
	 *       Especially the dot ('.') is not supported in the individual name segments,
	 *       as it is always interpreted as a name separator.
	 *
	 * @param {string} sName  a dot separated sequence of names that identify the property
	 * @param {any}    vValue value to be set, can have any type
	 * @param {object} [oContext=window] the context to execute the search in
	 * @public
	 * @static
	 */
	jQuery.sap.setObject = function (sName, vValue, oContext) {
		var oObject = oContext || window,
			aNames = (sName || "").split("."),
			l = aNames.length, i;

		if ( l > 0 ) {
			for (i = 0; oObject && i < l - 1; i++) {
				if (!oObject[aNames[i]] ) {
					oObject[aNames[i]] = {};
				}
				oObject = oObject[aNames[i]];
			}
			oObject[aNames[l - 1]] = vValue;
		}
	};

	// ---------------------- performance measurement -----------------------------------------------------------

	function PerfMeasurement() {

		function Measurement(sId, sInfo, iStart, iEnd, aCategories) {
			this.id = sId;
			this.info = sInfo;
			this.start = iStart;
			this.end = iEnd;
			this.pause = 0;
			this.resume = 0;
			this.duration = 0; // used time
			this.time = 0; // time from start to end
			this.categories = aCategories;
			this.average = false; //average duration enabled
			this.count = 0; //average count
			this.completeDuration = 0; //complete duration
		}

		function matchCategories(aCategories) {
			if (!aRestrictedCategories) {
				return true;
			}
			if (!aCategories) {
				return aRestrictedCategories === null;
			}
			//check whether active categories and current categories match
			for (var i = 0; i < aRestrictedCategories.length; i++) {
				if (aCategories.indexOf(aRestrictedCategories[i]) > -1) {
					return true;
				}
			}
			return false;
		}

		function checkCategories(aCategories) {
			if (!aCategories) {
				aCategories = ["javascript"];
			}
			aCategories = typeof aCategories === "string" ? aCategories.split(",") : aCategories;
			if (!matchCategories(aCategories)) {
				return null;
			}
			return aCategories;
		}

		function hasCategory(oMeasurement, aCategories) {
			for (var i = 0; i < aCategories.length; i++) {
				if (oMeasurement.categories.indexOf(aCategories[i]) > -1) {
					return true;
				}
			}
			return aCategories.length === 0;
		}

		var bActive = false,
			fnAjax = jQuery.ajax,
			aRestrictedCategories = null,
			aAverageMethods = [],
			aOriginalMethods = [],
			mMethods = {},
			mMeasurements = {};

		/**
		 * Gets the current state of the perfomance measurement functionality
		 *
		 * @return {boolean} current state of the perfomance measurement functionality
		 * @name jQuery.sap.measure#getActive
		 * @function
		 * @public
		 */
		this.getActive = function() {
			return bActive;
		};

		/**
		 * Activates or deactivates the performance measure functionality
		 * Optionally a category or list of categories can be passed to restrict measurements to certain categories
		 * like "javascript", "require", "xmlhttprequest", "render"
		 * @param {boolean} bOn state of the perfomance measurement functionality to set
		 * @param {string | string[]}  An optional list of categories that should be measured
		 *
		 * @return {boolean} current state of the perfomance measurement functionality
		 * @name jQuery.sap.measure#setActive
		 * @function
		 * @public
		 */
		this.setActive = function(bOn, aCategories) {
			//set restricted categories
			if (!aCategories) {
				aCategories = null;
			} else if (typeof aCategories === "string") {
				aCategories = aCategories.split(",");
			}
			aRestrictedCategories = aCategories;

			if (bActive === bOn) {
				return;
			}
			bActive = bOn;
			if (bActive) {

				//activate method implementations once
				for (var sName in mMethods) {
					this[sName] = mMethods[sName];
				}
				mMethods = {};
				// wrap and instrument jQuery.ajax
				jQuery.ajax = function(url, options) {

					if ( typeof url === 'object' ) {
						options = url;
						url = undefined;
					}
					options = options || {};

					var sMeasureId = new URI(url || options.url).absoluteTo(document.location.origin + document.location.pathname).href();
					jQuery.sap.measure.start(sMeasureId, "Request for " + sMeasureId, "xmlhttprequest");
					var fnComplete = options.complete;
					options.complete = function() {
						jQuery.sap.measure.end(sMeasureId);
						if (fnComplete) {
							fnComplete.apply(this, arguments);
						}
					};

					// strict mode: we potentially modified 'options', so we must not use 'arguments'
					return fnAjax.call(this, url, options);
				};
			} else if (fnAjax) {
				jQuery.ajax = fnAjax;
			}

			return bActive;
		};

		/**
		 * Starts a performance measure.
		 * Optionally a category or list of categories can be passed to allow filtering of measurements.
		 *
		 * @param {string} sId ID of the measurement
		 * @param {string} sInfo Info for the measurement
		 * @param {string | string[]} [aCategories = "javascript"] An optional list of categories for the measure
		 *
		 * @return {object} current measurement containing id, info and start-timestamp (false if error)
		 * @name jQuery.sap.measure#start
		 * @function
		 * @public
		 */
		mMethods["start"] = function(sId, sInfo, aCategories) {
			if (!bActive) {
				return;
			}

			aCategories = checkCategories(aCategories);
			if (!aCategories) {
				return;
			}

			var iTime = jQuery.sap.now(),
				oMeasurement = new Measurement( sId, sInfo, iTime, 0, aCategories);

			// create timeline entries if available
			/*eslint-disable no-console */
			if (jQuery.sap.log.getLevel("sap.ui.Performance") >= 4 && window.console && console.time) {
				console.time(sInfo + " - " + sId);
			}
			/*eslint-enable no-console */
//			jQuery.sap.log.info("Performance measurement start: "+ sId + " on "+ iTime);

			if (oMeasurement) {
				mMeasurements[sId] = oMeasurement;
				return this.getMeasurement(oMeasurement.id);
			} else {
				return false;
			}
		};

		/**
		 * Pauses a performance measure
		 *
		 * @param {string} sId ID of the measurement
		 * @return {object} current measurement containing id, info and start-timestamp, pause-timestamp (false if error)
		 * @name jQuery.sap.measure#pause
		 * @function
		 * @public
		 */
		mMethods["pause"] = function(sId) {
			if (!bActive) {
				return;
			}

			var iTime = jQuery.sap.now();
			var oMeasurement = mMeasurements[sId];
			if (oMeasurement && oMeasurement.end > 0) {
				// already ended -> no pause possible
				return false;
			}

			if (oMeasurement && oMeasurement.pause == 0) {
				// not already paused
				oMeasurement.pause = iTime;
				if (oMeasurement.pause >= oMeasurement.resume && oMeasurement.resume > 0) {
					oMeasurement.duration = oMeasurement.duration + oMeasurement.pause - oMeasurement.resume;
					oMeasurement.resume = 0;
				} else if (oMeasurement.pause >= oMeasurement.start) {
					oMeasurement.duration = oMeasurement.pause - oMeasurement.start;
				}
			}
//			jQuery.sap.log.info("Performance measurement pause: "+ sId + " on "+ iTime + " duration: "+ oMeasurement.duration);

			if (oMeasurement) {
				return this.getMeasurement(oMeasurement.id);
			} else {
				return false;
			}
		};

		/**
		 * Resumes a performance measure
		 *
		 * @param {string} sId ID of the measurement
		 * @return {object} current measurement containing id, info and start-timestamp, resume-timestamp (false if error)
		 * @name jQuery.sap.measure#resume
		 * @function
		 * @public
		 */
		mMethods["resume"] = function(sId) {
			if (!bActive) {
				return;
			}

			var iTime = jQuery.sap.now();
			var oMeasurement = mMeasurements[sId];
//			jQuery.sap.log.info("Performance measurement resume: "+ sId + " on "+ iTime + " duration: "+ oMeasurement.duration);

			if (oMeasurement && oMeasurement.pause > 0) {
				// already paused
				oMeasurement.pause = 0;
				oMeasurement.resume = iTime;
			}

			if (oMeasurement) {
				return this.getMeasurement(oMeasurement.id);
			} else {
				return false;
			}
		};

		/**
		 * Ends a performance measure
		 *
		 * @param {string} sId ID of the measurement
		 * @return {object} current measurement containing id, info and start-timestamp, end-timestamp, time, duration (false if error)
		 * @name jQuery.sap.measure#end
		 * @function
		 * @public
		 */
		mMethods["end"] = function(sId) {
			if (!bActive) {
				return;
			}

			var iTime = jQuery.sap.now();

			var oMeasurement = mMeasurements[sId];
//			jQuery.sap.log.info("Performance measurement end: "+ sId + " on "+ iTime);

			if (oMeasurement && !oMeasurement.end) {
				oMeasurement.end = iTime;
				if (oMeasurement.end >= oMeasurement.resume && oMeasurement.resume > 0) {
					oMeasurement.duration = oMeasurement.duration + oMeasurement.end - oMeasurement.resume;
					oMeasurement.resume = 0;
				} else if (oMeasurement.pause > 0) {
					// duration already calculated
					oMeasurement.pause = 0;
				} else if (oMeasurement.end >= oMeasurement.start) {
					if (oMeasurement.average) {
						oMeasurement.completeDuration += (oMeasurement.end - oMeasurement.start);
						oMeasurement.count++;
						oMeasurement.duration = oMeasurement.completeDuration / oMeasurement.count;
						oMeasurement.start = iTime;
					} else {
						oMeasurement.duration = oMeasurement.end - oMeasurement.start;
					}
				}
				if (oMeasurement.end >= oMeasurement.start) {
					oMeasurement.time = oMeasurement.end - oMeasurement.start;
				}
			}

			if (oMeasurement) {
				// end timeline entry
				/*eslint-disable no-console */
				if (jQuery.sap.log.getLevel("sap.ui.Performance") >= 4 && window.console && console.timeEnd) {
					console.timeEnd(oMeasurement.info + " - " + sId);
				}
				/*eslint-enable no-console */
				return this.getMeasurement(sId);
			} else {
				return false;
			}
		};

		/**
		 * Clears all performance measurements
		 *
		 * @name jQuery.sap.measure#clear
		 * @function
		 * @public
		 */
		mMethods["clear"] = function() {
			mMeasurements = {};
		};

		/**
		 * Removes a performance measure
		 *
		 * @param {string} sId ID of the measurement
		 * @name jQuery.sap.measure#remove
		 * @function
		 * @public
		 */
		mMethods["remove"] = function(sId) {
			delete mMeasurements[sId];
		};
		/**
		 * Adds a performance measurement with all data
		 * This is usefull to add external measurements (e.g. from a backend) to the common measurement UI
		 *
		 * @param {string} sId ID of the measurement
		 * @param {string} sInfo Info for the measurement
		 * @param {int} iStart start timestamp
		 * @param {int} iEnd end timestamp
		 * @param {int} iTime time in milliseconds
		 * @param {int} iDuration effective time in milliseconds
		 * @param {string | string[]} [aCategories = "javascript"] An optional list of categories for the measure
		 * @return {object} [] current measurement containing id, info and start-timestamp, end-timestamp, time, duration, categories (false if error)
		 * @name jQuery.sap.measure#add
		 * @function
		 * @public
		 */
		mMethods["add"] = function(sId, sInfo, iStart, iEnd, iTime, iDuration, aCategories) {
			if (!bActive) {
				return;
			}
			aCategories = checkCategories(aCategories);
			if (!aCategories) {
				return false;
			}
			var oMeasurement = new Measurement( sId, sInfo, iStart, iEnd, aCategories);
			oMeasurement.time = iTime;
			oMeasurement.duration = iDuration;

			if (oMeasurement) {
				mMeasurements[sId] = oMeasurement;
				return this.getMeasurement(oMeasurement.id);
			} else {
				return false;
			}
		};

		/**
		 * Starts an average performance measure.
		 * The duration of this measure is an avarage of durations measured for each call.
		 * Optionally a category or list of categories can be passed to allow filtering of measurements.
		 *
		 * @param {string} sId ID of the measurement
		 * @param {string} sInfo Info for the measurement
		 * @param {string | string[]} [aCategories = "javascript"] An optional list of categories for the measure
		 * @return {object} current measurement containing id, info and start-timestamp (false if error)
		 * @name jQuery.sap.measure#average
		 * @function
		 * @public
		 */
		mMethods["average"] = function(sId, sInfo, aCategories) {
			if (!bActive) {
				return;
			}
			aCategories = checkCategories(aCategories);
			if (!aCategories) {
				return;
			}

			var oMeasurement = mMeasurements[sId],
				iTime = jQuery.sap.now();
			if (!oMeasurement || !oMeasurement.average) {
				this.start(sId, sInfo, aCategories);
				oMeasurement = mMeasurements[sId];
				oMeasurement.average = true;
			} else {
				if (!oMeasurement.end) {
					oMeasurement.completeDuration += (iTime - oMeasurement.start);
					oMeasurement.count++;
				}
				oMeasurement.start = iTime;
				oMeasurement.end = 0;
			}
			return this.getMeasurement(oMeasurement.id);
		};

		/**
		 * Gets a performance measure
		 *
		 * @param {string} sId ID of the measurement
		 * @return {object} current measurement containing id, info and start-timestamp, end-timestamp, time, duration (false if error)
		 * @name jQuery.sap.measure#getMeasurement
		 * @function
		 * @public
		 */
		this.getMeasurement = function(sId) {

			var oMeasurement = mMeasurements[sId];

			if (oMeasurement) {
				// create a flat copy
				var oCopy = {};
				for (var sProp in oMeasurement) {
					oCopy[sProp] = oMeasurement[sProp];
				}
				return oCopy;
			} else {
				return false;
			}
		};

		/**
		 * Gets all performance measurements
		 *
		 * @param {boolean} [bCompleted] Whether only completed measurements should be returned, if explicitly set to false only incomplete measurements are returned
		 * @return {object[]} current array with measurements containing id, info and start-timestamp, end-timestamp, time, duration, categories
		 * @name jQuery.sap.measure#getAllMeasurements
		 * @function
		 * @public
		 */
		this.getAllMeasurements = function(bCompleted) {
			return this.filterMeasurements(function(oMeasurement) {
				return oMeasurement;
			}, bCompleted);
		};

		/**
		 * Gets all performance measurements where a provided filter function returns a truthy value.
		 * If neither a filter function nor a category is provided an empty array is returned.
		 * To filter for certain properties of measurements a fnFilter can be implemented like this
		 * <code>
		 * function(oMeasurement) {
		 *     return oMeasurement.duration > 50;
		 * }</code>
		 *
		 * @param {function} [fnFilter] a filter function that returns true if the passed measurement should be added to the result
		 * @param {boolean|undefined} [bCompleted] Optional parameter to determine if either completed or incomplete measurements should be returned (both if not set or undefined)
		 * @param {string[]} [aCategories] The function returns only measurements which match these specified categories
		 *
		 * @return {object} [] filtered array with measurements containing id, info and start-timestamp, end-timestamp, time, duration, categories (false if error)
		 * @name jQuery.sap.measure#filterMeasurements
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.filterMeasurements = function() {
			var oMeasurement, bValid,
				i = 0,
				aMeasurements = [],
				fnFilter = typeof arguments[i] === "function" ? arguments[i++] : undefined,
				bCompleted = typeof arguments[i] === "boolean" ? arguments[i++] : undefined,
				aCategories = Array.isArray(arguments[i]) ? arguments[i] : [];

			for (var sId in mMeasurements) {
				oMeasurement = this.getMeasurement(sId);
				bValid = (bCompleted === false && oMeasurement.end === 0) || (bCompleted !== false && (!bCompleted || oMeasurement.end));
				if (bValid && hasCategory(oMeasurement, aCategories) && (!fnFilter || fnFilter(oMeasurement))) {
					aMeasurements.push(oMeasurement);
				}
			}

			return aMeasurements;
		};

		/**
		 * Registers an average measurement for a given objects method
		 *
		 * @param {string} sId the id of the measurement
		 * @param {object} oObject the object of the method
		 * @param {string} sMethod the name of the method
		 * @param {string[]} [aCategories = ["javascript"]] An optional categories list for the measurement
		 *
		 * @returns {boolean} true if the registration was successful
		 * @name jQuery.sap.measure#registerMethod
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.registerMethod = function(sId, oObject, sMethod, aCategories) {
			var fnMethod = oObject[sMethod];
			if (fnMethod && typeof fnMethod === "function") {
				var bFound = aAverageMethods.indexOf(fnMethod) > -1;
				if (!bFound) {
					aOriginalMethods.push({func : fnMethod, obj: oObject, method: sMethod, id: sId});
					oObject[sMethod] = function() {
						jQuery.sap.measure.average(sId, sId + " method average", aCategories);
						var result = fnMethod.apply(this, arguments);
						jQuery.sap.measure.end(sId);
						return result;
					};
					aAverageMethods.push(oObject[sMethod]);
					return true;
				}
			} else {
				jQuery.sap.log.debug(sMethod + " in not a function. jQuery.sap.measure.register failed");
			}
			return false;
		};

		/**
		 * Unregisters an average measurement for a given objects method
		 *
		 * @param {string} sId the id of the measurement
		 * @param {object} oObject the object of the method
		 * @param {string} sMethod the name of the method
		 *
		 * @returns {boolean} true if the unregistration was successful
		 * @name jQuery.sap.measure#unregisterMethod
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.unregisterMethod = function(sId, oObject, sMethod) {
			var fnFunction = oObject[sMethod],
				iIndex = aAverageMethods.indexOf(fnFunction);
			if (fnFunction && iIndex > -1) {
				oObject[sMethod] = aOriginalMethods[iIndex].func;
				aAverageMethods.splice(iIndex, 1);
				aOriginalMethods.splice(iIndex, 1);
				return true;
			}
			return false;
		};

		/**
		 * Unregisters all average measurements
		 * @name jQuery.sap.measure#unregisterAllMethods
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.unregisterAllMethods = function() {
			while (aOriginalMethods.length > 0) {
				var oOrig = aOriginalMethods[0];
				this.unregisterMethod(oOrig.id, oOrig.obj, oOrig.method);
			}
		};

		// ** Interaction measure **
		var aInteractions = [];
		var oPendingInteraction;

		/**
		 * Gets all interaction measurements
		 * @param {boolean} bFinalize finalize the current pending interaction so that it is contained in the returned array
		 * @return {object[]} all interaction measurements
		 * @name jQuery.sap.measure#getAllInteractionMeasurements
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.getAllInteractionMeasurements = function(bFinalize) {
			if (bFinalize) {
				// force the finalization of the currently pending interaction
				jQuery.sap.measure.endInteraction(true);
			}
			return aInteractions;
		};

		/**
		 * Gets all interaction measurements for which a provided filter function returns a truthy value.
		 * To filter for certain categories of measurements a fnFilter can be implemented like this
		 * <code>
		 * function(oInteractionMeasurement) {
		 *     return oInteractionMeasurement.duration > 0
		 * }</code>
		 * @param {function} fnFilter a filter function that returns true if the passed measurement should be added to the result
		 * @return {object[]} all interaction measurements passing the filter function successfully
		 * @name jQuery.sap.measure#filterInteractionMeasurements
		 * @function
		 * @public
		 * @since 1.36.2
		 */
		this.filterInteractionMeasurements = function(fnFilter) {
			var aFilteredInteractions = [];
			if (fnFilter) {
				for (var i = 0, l = aInteractions.length; i < l; i++) {
					if (fnFilter(aInteractions[i])) {
						aFilteredInteractions.push(aInteractions[i]);
					}
				}
			}
			return aFilteredInteractions;
		};

		/**
		 * Gets the incomplete pending interaction
		 * @return {object} interaction measurement
		 * @name jQuery.sap.measure#getInteractionMeasurement
		 * @function
		 * @private
		 * @since 1.34.0
		 */
		this.getPendingInteractionMeasurement = function() {
			return oPendingInteraction;
		};

		/**
		 * Clears all interaction measurements
		 * @name jQuery.sap.measure#clearInteractionMeasurements
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.clearInteractionMeasurements = function() {
			aInteractions = [];
		};

		function isCompleteMeasurement(oMeasurement) {
			if (oMeasurement.start > oPendingInteraction.start && oMeasurement.end < oPendingInteraction.end) {
				return oMeasurement;
			}
		}

		function isCompleteTiming(oRequestTiming) {
			return oRequestTiming.startTime > 0 &&
				oRequestTiming.startTime <= oRequestTiming.requestStart &&
				oRequestTiming.requestStart <= oRequestTiming.responseEnd;
		}

		function aggregateRequestTiming(oRequest) {
			// aggregate navigation and roundtrip with respect to requests overlapping and times w/o requests (gaps)
			this.end = oRequest.responseEnd > this.end ? oRequest.responseEnd : this.end;
			// sum up request time as a grand total over all requests
			oPendingInteraction.requestTime += (oRequest.responseEnd - oRequest.startTime);

			// if there is a gap between requests we add the times to the aggrgate and shift the lower limits
			if (this.roundtripHigherLimit <= oRequest.startTime) {
				oPendingInteraction.navigation += (this.navigationHigherLimit - this.navigationLowerLimit);
				oPendingInteraction.roundtrip += (this.roundtripHigherLimit - this.roundtripLowerLimit);
				this.navigationLowerLimit = oRequest.startTime;
				this.roundtripLowerLimit = oRequest.startTime;
			}

			// shift the limits if this request was completed later than the earlier requests
			if (oRequest.responseEnd > this.roundtripHigherLimit) {
				this.roundtripHigherLimit = oRequest.responseEnd;
			}
			if (oRequest.requestStart > this.navigationHigherLimit) {
				this.navigationHigherLimit = oRequest.requestStart;
			}
		}

		function aggregateRequestTimings(aRequests) {
			var oTimings = {
				start: aRequests[0].startTime,
				end: aRequests[0].responseEnd,
				navigationLowerLimit: aRequests[0].startTime,
				navigationHigherLimit: aRequests[0].requestStart,
				roundtripLowerLimit: aRequests[0].startTime,
				roundtripHigherLimit: aRequests[0].responseEnd
			};

			// aggregate all timings by operating on the oTimings object
			aRequests.forEach(aggregateRequestTiming, oTimings);
			oPendingInteraction.navigation += (oTimings.navigationHigherLimit - oTimings.navigationLowerLimit);
			oPendingInteraction.roundtrip += (oTimings.roundtripHigherLimit - oTimings.roundtripLowerLimit);

			// calculate average network time per request
			if (oPendingInteraction.networkTime) {
				var iTotalNetworkTime = oPendingInteraction.requestTime - oPendingInteraction.networkTime;
				oPendingInteraction.networkTime = iTotalNetworkTime / aRequests.length;
			} else {
				oPendingInteraction.networkTime = 0;
			}

			// in case processing is not determined, which means no re-rendering occured, take start to end
			if (oPendingInteraction.processing === 0) {
				var iRelativeStart = oPendingInteraction.start - window.performance.timing.fetchStart;
				oPendingInteraction.duration = oTimings.end - iRelativeStart;
				// calculate processing time of before requests start
				oPendingInteraction.processing = oTimings.start - iRelativeStart;
			}

		}

		function finalizeInteraction(iTime) {
			if (oPendingInteraction) {
				oPendingInteraction.end = iTime;
				oPendingInteraction.duration = oPendingInteraction.processing;
				oPendingInteraction.requests = jQuery.sap.measure.getRequestTimings();
				oPendingInteraction.incompleteRequests = 0;
				oPendingInteraction.measurements = jQuery.sap.measure.filterMeasurements(isCompleteMeasurement, true);

				var aCompleteRequestTimings = oPendingInteraction.requests.filter(isCompleteTiming);
				if (aCompleteRequestTimings.length > 0) {
					aggregateRequestTimings(aCompleteRequestTimings);
					oPendingInteraction.incompleteRequests = oPendingInteraction.requests.length - aCompleteRequestTimings.length;
				}

				// calculate real processing time if any processing took place
				// cannot be negative as then requests took longer than processing
				var iProcessing = oPendingInteraction.processing - oPendingInteraction.navigation - oPendingInteraction.roundtrip;
				oPendingInteraction.processing = iProcessing > -1 ? iProcessing : 0;

				aInteractions.push(oPendingInteraction);
				jQuery.sap.log.info("Interaction step finished: trigger: " + oPendingInteraction.trigger + "; duration: " + oPendingInteraction.duration + "; requests: " + oPendingInteraction.requests.length, "jQuery.sap.measure");
				oPendingInteraction = null;
			}
		}

		// component determination - heuristic
		function createOwnerComponentInfo(oSrcElement) {
			var sId, sVersion;
			if (oSrcElement) {
				var Component, oComponent;
				Component = sap.ui.require("sap/ui/core/Component");
				while (Component && oSrcElement && oSrcElement.getParent) {
					oComponent = Component.getOwnerComponentFor(oSrcElement);
					if (oComponent || oSrcElement instanceof Component) {
						oComponent = oComponent || oSrcElement;
						var oApp = oComponent.getManifestEntry("sap.app");
						// get app id or module name for FESR
						sId = oApp && oApp.id || oComponent.getMetadata().getName();
						sVersion = oApp && oApp.applicationVersion && oApp.applicationVersion.version;
					}
					oSrcElement = oSrcElement.getParent();
				}
			}
			return {
				id: sId ? sId : "undetermined",
				version: sVersion ? sVersion : ""
			};
		}

		/**
		 * Start an interaction measurements
		 *
		 * @param {string} sType type of the event which triggered the interaction
		 * @param {object} oSrcElement the control on which the interaction was triggered
		 *
		 * @name jQuery.sap.measure#startInteraction
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.startInteraction = function(sType, oSrcElement) {
			var iTime = jQuery.sap.now();

			if (oPendingInteraction) {
				finalizeInteraction(iTime);
			}

			// clear request timings for new interaction
			this.clearRequestTimings();

			var oComponentInfo = createOwnerComponentInfo(oSrcElement);

			// setup new pending interaction
			oPendingInteraction = {
				event: sType, // event which triggered interaction
				trigger: oSrcElement && oSrcElement.getId ? oSrcElement.getId() : "undetermined", // control which triggered interaction
				component: oComponentInfo.id, // component or app identifier
				appVersion: oComponentInfo.version, // application version as from app descriptor
				start : iTime, // interaction start
				end: 0, // interaction end
				navigation: 0, // sum over all navigation times
				roundtrip: 0, // time from first request sent to last received response end - without gaps and ignored overlap
				processing: 0, // client processing time
				duration: 0, // interaction duration
				requests: [], // Performance API requests during interaction
				measurements: [], // jQuery.sap.measure Measurements
				sapStatistics: [], // SAP Statistics for OData, added by jQuery.sap.trace
				requestTime: 0, // summ over all requests in the interaction (oPendingInteraction.requests[0].responseEnd-oPendingInteraction.requests[0].requestStart)
				networkTime: 0, // request time minus server time from the header, added by jQuery.sap.trace
				bytesSent: 0, // sum over all requests bytes, added by jQuery.sap.trace
				bytesReceived: 0, // sum over all response bytes, added by jQuery.sap.trace
				requestCompression: undefined, // true if all responses have been sent gzipped
				busyDuration : 0 // summed GlobalBusyIndicator duration during this interaction
			};
			jQuery.sap.log.info("Interaction step started: trigger: " + oPendingInteraction.trigger + "; type: " + oPendingInteraction.event, "jQuery.sap.measure");
		};

		/**
		 * End an interaction measurements
		 *
		 * @param {boolean} bForce forces end of interaction now and ignores further re-renderings
		 *
		 * @name jQuery.sap.measure#endInteraction
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.endInteraction = function(bForce) {
			if (oPendingInteraction) {
				// set provisionary processing time from start to end and calculate later
				if (!bForce) {
					oPendingInteraction.processing = jQuery.sap.now() - oPendingInteraction.start;
				} else {
					finalizeInteraction(jQuery.sap.now());
				}
			}
		};

		/**
		 * Sets the request buffer size for the measurement safely
		 *
		 * @param {int} iSize size of the buffer
		 *
		 * @name jQuery.sap.measure#setRequestBufferSize
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.setRequestBufferSize = function(iSize) {
			if (!window.performance) {
				return;
			}
			if (window.performance.setResourceTimingBufferSize) {
				window.performance.setResourceTimingBufferSize(iSize);
			} else if (window.performance.webkitSetResourceTimingBufferSize) {
				window.performance.webkitSetResourceTimingBufferSize(iSize);
			}
		};

		/**
		 * Gets the current request timings array for type 'resource' safely
		 *
		 * @return {object[]} array of performance timing objects
		 * @name jQuery.sap.measure#getRequestTimings
		 * @function
		 * @public
		 * @since 1.34.0
		 */
		this.getRequestTimings = function() {
			if (window.performance && window.performance.getEntriesByType) {
				return window.performance.getEntriesByType("resource");
			}
			return [];
		};

		 /**
			 * Clears all request timings safely
			 *
			 * @name jQuery.sap.measure#clearRequestTimings
			 * @function
			 * @public
			 * @since 1.34.0
			 */
		this.clearRequestTimings = function() {
			if (!window.performance) {
				return;
			}
			if (window.performance.clearResourceTimings) {
				window.performance.clearResourceTimings();
			} else if (window.performance.webkitClearResourceTimings){
				window.performance.webkitClearResourceTimings();
			}
		};

		this.setRequestBufferSize(1000);

		var aMatch = location.search.match(/sap-ui-measure=([^\&]*)/);
		if (aMatch && aMatch[1]) {
			if (aMatch[1] === "true" || aMatch[1] === "x" || aMatch[1] === "X") {
				this.setActive(true);
			} else {
				this.setActive(true, aMatch[1]);
			}
		} else {
			var fnInactive = function() {
				//measure not active
				return null;
			};
			//deactivate methods implementations
			for (var sName in mMethods) {
				this[sName] = fnInactive;
			}
		}
	}

	/**
	 * Namespace for the jQuery performance measurement plug-in provided by SAP SE.
	 *
	 * @namespace
	 * @name jQuery.sap.measure
	 * @public
	 * @static
	 */
	jQuery.sap.measure = new PerfMeasurement();

	// ---------------------- sync point -------------------------------------------------------------

	/*
	 * Internal class that can help to synchronize a set of asynchronous tasks.
	 * Each task must be registered in the sync point by calling startTask with
	 * an (purely informative) title. The returned value must be used in a later
	 * call to finishTask.
	 * When finishTask has been called for all tasks that have been started,
	 * the fnCallback will be fired.
	 * When a timeout is given and reached, the callback is called at that
	 * time, no matter whether all tasks have been finished or not.
	 */
	function SyncPoint(sName, fnCallback, iTimeout) {
		var aTasks = [],
			iOpenTasks = 0,
			iFailures = 0,
			sTimer;

		this.startTask = function(sTitle) {
			var iId = aTasks.length;
			aTasks[iId] = { name : sTitle, finished : false };
			iOpenTasks++;
			return iId;
		};

		this.finishTask = function(iId, bSuccess) {
			if ( !aTasks[iId] || aTasks[iId].finished ) {
				throw new Error("trying to finish non existing or already finished task");
			}
			aTasks[iId].finished = true;
			iOpenTasks--;
			if ( bSuccess === false ) {
				iFailures++;
			}
			if ( iOpenTasks === 0 ) {
				jQuery.sap.log.info("Sync point '" + sName + "' finished (tasks:" + aTasks.length + ", open:" + iOpenTasks + ", failures:" + iFailures + ")");
				if ( sTimer ) {
					clearTimeout(sTimer);
					sTimer = null;
				}
				finish();
			}
		};

		function finish() {
			fnCallback && fnCallback(iOpenTasks, iFailures);
			fnCallback = null;
		}

		if ( !isNaN(iTimeout) ) {
			sTimer = setTimeout(function() {
				jQuery.sap.log.info("Sync point '" + sName + "' timed out (tasks:" + aTasks.length + ", open:" + iOpenTasks + ", failures:" + iFailures + ")");
				finish();
			}, iTimeout);
		}

		jQuery.sap.log.info("Sync point '" + sName + "' created" + (iTimeout ? "(timeout after " + iTimeout + " ms)" : ""));

	}

	/**
	 * Internal function to create a sync point.
	 * @private
	 */
	jQuery.sap.syncPoint = function(sName, fnCallback, iTimeout) {
		return new SyncPoint(sName, fnCallback, iTimeout);
	};

	// ---------------------- require/declare --------------------------------------------------------

	var getModuleSystemInfo = (function() {

		/**
		 * Local logger, by default only logging errors. Can be configured to DEBUG via config parameter.
		 * @private
		 */
		var log = jQuery.sap.log.getLogger("sap.ui.ModuleSystem",
				(/sap-ui-xx-debug(M|-m)odule(L|-l)oading=(true|x|X)/.test(location.search) || oCfgData["xx-debugModuleLoading"]) ? jQuery.sap.log.Level.DEBUG : jQuery.sap.log.Level.INFO
			),

		/**
		 * A map of URL prefixes keyed by the corresponding module name prefix.
		 * URL prefix can either be given as string or as object with properties url and final.
		 * When final is set to true, module name prefix cannot be overwritten.
		 * @see jQuery.sap.registerModulePath
		 *
		 * Note that the empty prefix ('') will always match and thus serves as a fallback.
		 * @private
		 */
			mUrlPrefixes = { '' : { 'url' : 'resources/' } },

		/**
		 * Module neither has been required nor preloaded not declared, but someone asked for it.
		 */
			INITIAL = 0,

		/**
		 * Module has been preloaded, but not required or declared
		 */
			PRELOADED = -1,

		/**
		 * Module has been declared.
		 */
			LOADING = 1,

		/**
		 * Module has been loaded, but not yet executed.
		 */
			LOADED = 2,

		/**
		 * Module is currently being executed
		 */
			EXECUTING = 3,

		/**
		 * Module has been loaded and executed without errors.
		 */
			READY = 4,

		/**
		 * Module either could not be loaded or execution threw an error
		 */
			FAILED = 5,

		/**
		 * Special content value used internally until the content of a module has been determined
		 */
			NOT_YET_DETERMINED = {},

		/**
		 * Set of modules that have been loaded (required) so far.
		 *
		 * Each module is an object that can have the following members
		 * <ul>
		 * <li>{int} state one of the module states defined in this function
		 * <li>{string} url URL where the module has been loaded from
		 * <li>{any} data temp. raw content of the module (between loaded and ready)
		 * <li>{string} error an error description for state <code>FAILED</code>
		 * <li>{any} content the content of the module as exported via define()
		 * </ul>
		 * @private
		 */
			mModules = {},

			mPreloadModules = {},

		/**
		 * Whether sap.ui.define calls could be executed asynchronously in the current context.
		 *
		 * The initial value is determined by the preload flag. This is necessary to make
		 * hard coded script tags work when their scripts include a sap.ui.define call and if
		 * some later incline script expects the results of sap.ui.define.
		 * Most prominent example: unit tests that include QUnitUtils as a script tag and use qutils
		 * in one of their inline scripts.
		 */
			bGlobalAsyncMode = !( /(?:^|\?|&)sap-ui-(?:xx-)?preload=async(?:&|$)/.test(location.search) || oCfgData.preload === 'async' || oCfgData['xx-preload'] === 'async'),

		/* for future use
		/**
		 * Mapping from default AMD names to UI5 AMD names.
		 *
		 * For simpler usage in requireModule, the names are already converted to
		 * normalized resource names.
		 *
		 * /
			mAMDAliases = {
				'blanket.js': 'sap/ui/thirdparty/blanket.js',
				'crossroads.js': 'sap/ui/thirdparty/crossroads.js',
				'd3.js': 'sap/ui/thirdparty/d3.js',
				'handlebars.js': 'sap/ui/thirdparty/handlebars.js',
				'hasher.js': 'sap/ui/thirdparty/hasher.js',
				'IPv6.js': 'sap/ui/thirdparty/IPv6.js',
				'jquery.js': 'sap/ui/thirdparty/jquery.js',
				'jszip.js': 'sap/ui/thirdparty/jszip.js',
				'less.js': 'sap/ui/thirdparty/less.js',
				'OData.js': 'sap/ui/thirdparty/datajs.js',
				'punycode.js': 'sap/ui/thirdparty/punycode.js',
				'SecondLevelDomains.js': 'sap/ui/thirdparty/SecondLevelDomains.js',
				'sinon.js': 'sap/ui/thirdparty/sinon.js',
				'signals.js': 'sap/ui/thirdparty/signals.js',
				'URI.js': 'sap/ui/thirdparty/URI.js',
				'URITemplate.js': 'sap/ui/thirdparty/URITemplate.js',
				'esprima.js': 'sap/ui/demokit/js/esprima.js'
			},
		*/

		/**
		 * Information about third party modules, keyed by the module's resource name (including extension '.js').
		 *
		 * Note that the stored dependencies also include a '.js' for easier evaluation, but the
		 * <code>registerModuleShims</code> method expects all names without the extension for better
		 * compatibility with the requireJS configuration.
		 *
		 * @see jQuery.sap.registerModuleShims
		 * @private
		 */
			mAMDShim = {
				'sap/ui/thirdparty/blanket.js': {
					amd: true,
					exports: 'blanket' // '_blanket', 'esprima', 'falafel', 'inBrowser', 'parseAndModify'
				},
				'sap/ui/thirdparty/caja-html-sanitizer.js': {
					amd: false,
					exports: 'html' // 'html_sanitizer', 'html4'
				},
				'sap/ui/thirdparty/crossroads.js': {
					amd: true,
					exports: 'crossroads',
					deps: ['sap/ui/thirdparty/signals']
				},
				'sap/ui/thirdparty/d3.js': {
					amd: true,
					exports: 'd3'
				},
				'sap/ui/thirdparty/datajs.js': {
					amd: true,
					exports: 'OData' // 'datajs'
				},
				'sap/ui/thirdparty/es6-promise.js': {
					amd: true,
					exports: 'ES6Promise'
				},
				'sap/ui/thirdparty/flexie.js': {
					exports: 'Flexie'
				},
				'sap/ui/thirdparty/handlebars.js': {
					amd: true,
					exports: 'Handlebars'
				},
				'sap/ui/thirdparty/hasher.js': {
					amd: true,
					exports: 'hasher',
					deps: ['sap/ui/thirdparty/signals']
				},
				'sap/ui/thirdparty/IPv6.js': {
					amd: true,
					exports: 'IPv6'
				},
				'sap/ui/thirdparty/iscroll-lite.js': {
					exports: 'iScroll'
				},
				'sap/ui/thirdparty/iscroll.js': {
					exports: 'iScroll'
				},
				'sap/ui/thirdparty/jquery.js': {
					amd: true
				},
				'sap/ui/thirdparty/jquery-mobile-custom.js': {
					amd: true,
					exports: 'jQuery.mobile'
				},
				'sap/ui/thirdparty/jszip.js': {
					amd: true,
					exports: 'JSZip'
				},
				'sap/ui/thirdparty/less.js': {
					amd: true,
					exports: 'less'
				},
				'sap/ui/thirdparty/mobify-carousel.js': {
					exports: 'Mobify' // or Mobify.UI.Carousel?
				},
				'sap/ui/thirdparty/punycode.js': {
					amd: true,
					exports: 'punycode'
				},
				'sap/ui/thirdparty/require.js': {
					exports: 'define' // 'require', 'requirejs'
				},
				'sap/ui/thirdparty/SecondLevelDomains.js': {
					amd: true,
					exports: 'SecondLevelDomains'
				},
				'sap/ui/thirdparty/signals.js': {
					amd: true,
					exports: 'signals'
				},
				'sap/ui/thirdparty/sinon.js': {
					amd: true,
					exports: 'sinon'
				},
				'sap/ui/thirdparty/sinon-server.js': {
					amd: true,
					exports: 'sinon' // really sinon! sinon-server is a subset of server and uses the same global for export
				},
				'sap/ui/thirdparty/unorm.js': {
					exports: 'UNorm'
				},
				'sap/ui/thirdparty/unormdata.js': {
					exports: 'UNorm', // really 'UNorm'! module extends UNorm
					deps: ['sap/ui/thirdparty/unorm']
				},
				'sap/ui/thirdparty/URI.js': {
					amd: true,
					exports: 'URI'
				},
				'sap/ui/thirdparty/URITemplate.js': {
					amd: true,
					exports: 'URITemplate',
					deps: ['sap/ui/thirdparty/URI']
				},
				'sap/ui/thirdparty/vkbeautify.js': {
					exports: 'vkbeautify'
				},
				'sap/ui/thirdparty/zyngascroll.js': {
					exports: 'Scroller' // 'requestAnimationFrame', 'cancelRequestAnimationFrame', 'core'
				},
				'sap/ui/demokit/js/esprima.js': {
					amd: true,
					exports: 'esprima'
				}
			},

		/**
		 * Stack of modules that are currently executed.
		 *
		 * Allows to identify the containing module in case of multi module files (e.g. sap-ui-core)
		 * @private
		 */
			_execStack = [ ],

		/**
		 * A prefix that will be added to module loading log statements and which reflects the nesting of module executions.
		 * @private
		 */
			sLogPrefix = "",

		// max size a script should have when executing it with execScript (IE). Otherwise fallback to eval
			MAX_EXEC_SCRIPT_LENGTH = 512 * 1024,

			sDocumentLocation = document.location.href.replace(/\?.*|#.*/g, ""),

			FRAGMENT = "fragment",
			VIEW = "view",
			mKnownSubtypes = {
				js :  [VIEW, FRAGMENT, "controller", "designtime"],
				xml:  [VIEW, FRAGMENT],
				json: [VIEW, FRAGMENT],
				html: [VIEW, FRAGMENT]
			},

			rJSSubtypes = new RegExp("(\\.(?:" + mKnownSubtypes.js.join("|") + "))?\\.js$"),
			rTypes,
			rSubTypes;

		(function() {
			var s = "",
				sSub = "";

			jQuery.each(mKnownSubtypes, function(sType, aSubtypes) {
				s = (s ? s + "|" : "") + sType;
				sSub = (sSub ? sSub + "|" : "") + "(?:(?:" + aSubtypes.join("\\.|") + "\\.)?" + sType + ")";
			});
			s = "\\.(" + s + ")$";
			sSub = "\\.(?:" + sSub + "|[^./]+)$";
			log.debug("constructed regexp for file types :" + s);
			log.debug("constructed regexp for file sub-types :" + sSub);
			rTypes = new RegExp(s);
			rSubTypes = new RegExp(sSub);
		}());

		/**
		 * When defined, checks whether preload should be ignored for the given module.
		 * If undefined, all preloads will be used.
		 */
		var fnIgnorePreload;

		(function() {
			var vDebugInfo = window["sap-ui-debug"];

			function makeRegExp(sGlobPattern) {
				if ( !/\/\*\*\/$/.test(sGlobPattern) ) {
					sGlobPattern = sGlobPattern.replace(/\/$/, '/**/');
				}
				return sGlobPattern.replace(/\*\*\/|\*|[[\]{}()+?.\\^$|]/g, function(sMatch) {
					switch (sMatch) {
						case '**/' : return '(?:[^/]+/)*';
						case '*'   : return '[^/]*';
						default    : return '\\' + sMatch;
					}
				});
			}

			if ( typeof vDebugInfo === 'string' ) {
				var sPattern =  "^(?:" + vDebugInfo.split(/,/).map(makeRegExp).join("|") + ")",
					rFilter = new RegExp(sPattern);

				fnIgnorePreload = function(sModuleName) {
					return rFilter.test(sModuleName);
				};

				log.debug("Modules that should be excluded from preload: '" + sPattern + "'");

			} else if ( vDebugInfo === true ) {

				fnIgnorePreload = function() {
					return true;
				};

				log.debug("All modules should be excluded from preload");

			}
		})();

		/**
		 * A module/resource as managed by the module system.
		 *
		 * Each module is an object with the following properties
		 * <ul>
		 * <li>{int} state one of the module states defined in this function
		 * <li>{string} url URL where the module has been loaded from
		 * <li>{any} data temp. raw content of the module (between loaded and ready or when preloaded)
		 * <li>{string} group the bundle with which a resource was loaded or null
		 * <li>{string} error an error description for state <code>FAILED</code>
		 * <li>{any} content the content of the module as exported via define()
		 * </ul>
		 */
		function Module(name) {
			this.name = name;
			this.state = INITIAL;
			this.url =
			this.loaded =
			this.data =
			this.group = null;
			this.content = NOT_YET_DETERMINED;
		}

		Module.prototype.ready = function(url, content) {
			if ( this.state === INITIAL ) {
				this.state = READY;
				this.url = url;
				this.content = content;
			}
			return this;
		};

		Module.prototype.preload = function(url, data, bundle) {
			if ( this.state === INITIAL && !(fnIgnorePreload && fnIgnorePreload(this.name)) ) {
				this.state = PRELOADED;
				this.url = url;
				this.data = data;
				this.group = bundle;
			}
			return this;
		};

		Module.get = function(sModuleName) {
			return mModules[sModuleName] || (mModules[sModuleName] = new Module(sModuleName));
		};

		/**
		 * Determines the value of this module.
		 *
		 * If the module hasn't been loaded or executed yet, <code>undefined</code> will be returned.
		 *
		 * @private
		 */
		Module.prototype.value = function() {

			if ( this.state === READY ) {
				if ( this.content === NOT_YET_DETERMINED ) {
					// Determine the module value lazily.
					// For AMD modules this has already been done on execution of the factory function.
					// For other modules that are required individually, it has been done after execution.
					// For the few remaining scenarios (like old-fashioned 'library-all' bundles), it is done here
					var oShim = mAMDShim[this.name],
						sExport = oShim && (Array.isArray(oShim.exports) ? oShim.exports[0] : oShim.exports);
					// best guess for thirdparty modules or legacy modules that don't use sap.ui.define
					this.content = jQuery.sap.getObject( sExport || urnToUI5(this.name) );
				}
				return this.content;
			}

			return; // undefined
		};

		// predefine already loaded modules to avoid redundant loading
		// Module.get("sap/ui/thirdparty/jquery.js").ready(_sBootstrapUrl, jQuery);
		Module.get("sap/ui/thirdparty/URI.js").ready(_sBootstrapUrl, URI);
		Module.get("sap/ui/Device.js").ready(_sBootstrapUrl, Device);
		Module.get("jquery.sap.global.js").ready(_sBootstrapUrl, jQuery);

		/**
		 * Name conversion function that converts a name in UI5 module name syntax to a name in requireJS module name syntax.
		 * @private
		 */
		function ui5ToRJS(sName) {
			if ( /^jquery\.sap\./.test(sName) ) {
				return sName;
			}
			return sName.replace(/\./g, "/");
		}

		/**
		 * Name conversion function that converts a name in unified resource name syntax to a name in UI5 module name syntax.
		 * If the name cannot be converted (e.g. doesn't end with '.js'), then <code>undefined</code> is returned.
		 *
		 * @private
		 */
		function urnToUI5(sName) {
			// UI5 module name syntax is only defined for JS resources
			if ( !/\.js$/.test(sName) ) {
				return;
			}

			sName = sName.slice(0, -3);
			if ( /^jquery\.sap\./.test(sName) ) {
				return sName; // do nothing
			}
			return sName.replace(/\//g, ".");
		}

		// find longest matching prefix for resource name
		function getResourcePath(sResourceName, sSuffix) {

			// split name into segments
			var aSegments = sResourceName.split(/\//),
				l, sNamePrefix, sResult, m;

			// if no suffix was given and if the name is not empty, try to guess the suffix from the last segment
			if ( arguments.length === 1  &&  aSegments.length > 0 ) {
				// only known types (and their known subtypes) are accepted
				m = rSubTypes.exec(aSegments[aSegments.length - 1]);
				if ( m ) {
					sSuffix = m[0];
					aSegments[aSegments.length - 1] = aSegments[aSegments.length - 1].slice(0, m.index);
				} else {
					sSuffix = "";
				}
			}

			// search for a defined name prefix, starting with the full name and successively removing one segment
			for (l = aSegments.length; l >= 0; l--) {
				sNamePrefix = aSegments.slice(0, l).join('/');
				if ( mUrlPrefixes[sNamePrefix] ) {
					sResult = mUrlPrefixes[sNamePrefix].url;
					if ( l < aSegments.length ) {
						sResult += aSegments.slice(l).join('/');
					}
					if ( sResult.slice(-1) === '/' ) {
						sResult = sResult.slice(0, -1);
					}
					return sResult + (sSuffix || '');
				}
			}

			jQuery.sap.assert(false, "should never happen");
		}

		function guessResourceName(sURL) {
			var sNamePrefix,
				sUrlPrefix,
				sResourceName;

			for (sNamePrefix in mUrlPrefixes) {
				if ( mUrlPrefixes.hasOwnProperty(sNamePrefix) ) {

					// Note: configured URL prefixes are guaranteed to end with a '/'
					// But to support the legacy scenario promoted by the application tools ( "registerModulePath('Application','Application')" )
					// the prefix check here has to be done without the slash
					sUrlPrefix = mUrlPrefixes[sNamePrefix].url.slice(0, -1);

					if ( sURL.indexOf(sUrlPrefix) === 0 ) {

						// calc resource name
						sResourceName = sNamePrefix + sURL.slice(sUrlPrefix.length);
						// remove a leading '/' (occurs if name prefix is empty and if match was a full segment match
						if ( sResourceName.charAt(0) === '/' ) {
							sResourceName = sResourceName.slice(1);
						}

						if ( mModules[sResourceName] && mModules[sResourceName].data ) {
							return sResourceName;
						}
					}
				}
			}

			// return undefined;
		}

		function extractStacktrace(oError) {
			if (!oError.stack) {
				try {
					throw oError;
				} catch (ex) {
					return ex.stack;
				}
			}
			return oError.stack;
		}

		function enhanceStacktrace(oError, oCausedByStack) {
			// concat the error stack for better traceability of loading issues
			// (ignore for PhantomJS since Error.stack is readonly property!)
			if (!Device.browser.phantomJS) {
				var oErrorStack = extractStacktrace(oError);
				if (oErrorStack && oCausedByStack) {
					oError.stack = oErrorStack + "\nCaused by: " + oCausedByStack;
				}
			}
			// for non Chrome browsers we log the caused by stack manually in the console
			if (window.console && !Device.browser.chrome) {
				/*eslint-disable no-console */
				console.error(oError.message + "\nCaused by: " + oCausedByStack);
				/*eslint-enable no-console */
			}
		}

		var rDotsAnywhere = /(?:^|\/)\.+/;
		var rDotSegment = /^\.*$/;

		/**
		 * Resolves relative module names that contain <code>./</code> or <code>../</code> segments to absolute names.
		 * E.g.: A name <code>../common/validation.js</code> defined in <code>sap/myapp/controller/mycontroller.controller.js</code>
		 * may resolve to <code>sap/myapp/common/validation.js</code>.
		 *
		 * When sBaseName is <code>null</code>, relative names are not allowed (e.g. for a <code>sap.ui.require</code> call)
		 * and their usage results in an error being thrown.
		 *
		 * @param {string|null} sBaseName name of a reference module
		 * @param {string} sModuleName the name to resolve
		 * @returns {string} resolved name
		 * @private
		 */
		function resolveModuleName(sBaseName, sModuleName) {

			var m = rDotsAnywhere.exec(sModuleName),
				aSegments,
				sSegment,
				i,j,l;

			// check whether the name needs to be resolved at all - if not, just return the sModuleName as it is.
			if ( !m ) {
				return sModuleName;
			}

			// if the name starts with a relative segments then there must be a base name (a global sap.ui.require doesn't support relative names)
			if ( m.index === 0 && sBaseName == null ) {
				throw new Error("relative name not supported ('" + sModuleName + "'");
			}

			// if relative name starts with a dot segment, then prefix it with the base path
			aSegments = (m.index === 0 ? sBaseName + sModuleName : sModuleName).split('/');

			// process path segments
			for (i = 0, j = 0, l = aSegments.length; i < l; i++) {

				var sSegment = aSegments[i];

				if ( rDotSegment.test(sSegment) ) {
					if (sSegment === '.' || sSegment === '') {
						// ignore '.' as it's just a pointer to current package. ignore '' as it results from double slashes (ignored by browsers as well)
						continue;
					} else if (sSegment === '..') {
						// move to parent directory
						if ( j === 0 ) {
							throw new Error("Can't navigate to parent of root (base='" + sBaseName + "', name='" + sModuleName + "'");//  sBaseNamegetPackagePath(), relativePath));
						}
						j--;
					} else {
						throw new Error("illegal path segment '" + sSegment + "'");
					}
				} else {

					aSegments[j++] = sSegment;

				}

			}

			aSegments.length = j;

			return aSegments.join('/');
		}

		function declareModule(sModuleName) {
			var oModule;

			// sModuleName must be a unified resource name of type .js
			jQuery.sap.assert(/\.js$/.test(sModuleName), "must be a Javascript module");

			oModule = Module.get(sModuleName);

			if ( oModule.state > INITIAL ) {
				return oModule;
			}

			if ( log.isLoggable() ) {
				log.debug(sLogPrefix + "declare module '" + sModuleName + "'");
			}

			// avoid cycles
			oModule.state = READY;

			// the first call to declareModule is assumed to identify the bootstrap module
			// Note: this is only a guess and fails e.g. when multiple modules are loaded via a script tag
			// to make it safe, we could convert 'declare' calls to e.g. 'subdeclare' calls at build time.
			if ( _execStack.length === 0 ) {
				_execStack.push(sModuleName);
				oModule.url = oModule.url || _sBootstrapUrl;
			}

			return oModule;
		}

		function requireModule(oRequestingModule, sModuleName, bAsync) {

			// TODO enable when preload has been adapted:
			// sModuleName = mAMDAliases[sModuleName] || sModuleName;

			var bLoggable = log.isLoggable(),
				m = rJSSubtypes.exec(sModuleName),
				oShim = mAMDShim[sModuleName],
				sBaseName, sType, oModule, aExtensions, i, sMsg;

			// only for robustness, should not be possible by design (all callers append '.js')
			if ( !m ) {
				throw new Error("can only require Javascript module, not " + sModuleName);
			}

			oModule = Module.get(sModuleName);

			if ( oShim && oShim.deps && !oShim.deps.requested ) {
				if ( bLoggable ) {
					log.debug("require dependencies of raw module " + sModuleName);
				}
				return requireAll(oModule, oShim.deps, function() {
					oShim.deps.requested = true;
					return requireModule(oRequestingModule, sModuleName, bAsync);
				}, bAsync);
			}

			// in case of having a type specified ignore the type for the module path creation and add it as file extension
			sBaseName = sModuleName.slice(0, m.index);
			sType = m[0]; // must be a normalized resource name of type .js sType can be one of .js|.view.js|.controller.js|.fragment.js|.designtime.js

			if ( bLoggable ) {
				log.debug(sLogPrefix + "require '" + sModuleName + "' of type '" + sType + "'");
			}

			// check if module has been loaded already
			if ( oModule.state !== INITIAL ) {
				if ( oModule.state === PRELOADED ) {
					oModule.state = LOADED;
					jQuery.sap.measure.start(sModuleName, "Require module " + sModuleName + " (preloaded)", ["require"]);
					execModule(sModuleName, bAsync);
					jQuery.sap.measure.end(sModuleName);
				}

				if ( oModule.state === READY ) {
					if ( bLoggable ) {
						log.debug(sLogPrefix + "module '" + sModuleName + "' has already been loaded (skipped).");
					}
					return oModule.value();
				} else if ( oModule.state === FAILED ) {
					var oError = new Error("found in negative cache: '" + sModuleName +  "' from " + oModule.url + ": " + oModule.errorMessage);
					enhanceStacktrace(oError, oModule.errorStack);
					throw oError;
				} else {
					// currently loading
					return;
				}
			}

			jQuery.sap.measure.start(sModuleName, "Require module " + sModuleName, ["require"]);

			// set marker for loading modules (to break cycles)
			oModule.state = LOADING;
			// if debug is enabled, try to load debug module first
			aExtensions = window["sap-ui-loaddbg"] ? ["-dbg", ""] : [""];
			for (i = 0; i < aExtensions.length && oModule.state !== LOADED; i++) {
				// create module URL for the current extension
				oModule.url = getResourcePath(sBaseName, aExtensions[i] + sType);
				if ( bLoggable ) {
					log.debug(sLogPrefix + "loading " + (aExtensions[i] ? aExtensions[i] + " version of " : "") + "'" + sModuleName + "' from '" + oModule.url + "'");
				}

				if ( !bAsync && syncCallBehavior && sModuleName !== 'sap/ui/core/Core.js' ) {
					sMsg = "[nosync] loading module '" + oModule.url + "'";
					if ( syncCallBehavior === 1 ) {
						log.error(sMsg);
					} else {
						throw new Error(sMsg);
					}
				}

				/*eslint-disable no-loop-func */
				jQuery.ajax({
					url : oModule.url,
					dataType : 'text',
					async : false,
					success : function(response, textStatus, xhr) {
						oModule.state = LOADED;
						oModule.data = response;
					},
					error : function(xhr, textStatus, error) {
						oModule.state = FAILED;
						oModule.errorMessage = xhr ? xhr.status + " - " + xhr.statusText : textStatus;
						oModule.errorStack = error && error.stack;
						oModule.loadError = true;
					}
				});
				/*eslint-enable no-loop-func */
			}
			// execute module __after__ loading it, this reduces the required stack space!
			if ( oModule.state === LOADED ) {
				execModule(sModuleName, bAsync);
			}

			jQuery.sap.measure.end(sModuleName);

			if ( oModule.state !== READY ) {
				var oError = new Error("failed to load '" + sModuleName +  "' from " + oModule.url + ": " + oModule.errorMessage);
				enhanceStacktrace(oError, oModule.errorStack);
				oError.loadError = oModule.loadError;
				throw oError;
			}

			return oModule.value();
		}

		/**
		 * Executes the wrapper function around a preloaded, non-AMD module.
		 * The only purpose of this function is to isolate the execution time of function parsing in performance measurements.
		 * @no-rename
		 * @private
		 */
		function callPreloadWrapperFn(fn) {
			callPreloadWrapperFn.count++;
			return fn.call(window);
		}
		callPreloadWrapperFn.count = 0;

		/**
		 * Executes the factory function for an AMD-module.
		 * The only purpose of this function is to isolate the execution time of function parsing in performance measurements.
		 * @no-rename
		 * @private
		 */
		function applyAMDFactoryFn(fn, dep) {
			applyAMDFactoryFn.count++;
			return fn.apply(window, dep);
		}
		applyAMDFactoryFn.count = 0;

		/**
		 * Evaluates the script for a loaded or preloaded module.
		 * The only purpose of this function is to isolate the execution time of string parsing in performance measurements.
		 * @no-rename
		 * @private
		 */
		function evalModuleStr(script) {
			evalModuleStr.count++;
			return window.eval(script);
		}
		evalModuleStr.count = 0;

		// sModuleName must be a normalized resource name of type .js
		function execModule(sModuleName, bAsync) {

			var oModule = mModules[sModuleName],
				oShim = mAMDShim[sModuleName],
				bLoggable = log.isLoggable(),
				sOldPrefix, sScript, vAMD, oMatch, bOldGlobalAsyncMode;

			if ( oModule && oModule.state === LOADED && typeof oModule.data !== "undefined" ) {

				// check whether the module is known to use an existing AMD loader, remember the AMD flag
				vAMD = (oShim === true || (oShim && oShim.amd)) && typeof window.define === "function" && window.define.amd;
				bOldGlobalAsyncMode = bGlobalAsyncMode;

				try {

					if ( vAMD ) {
						// temp. remove the AMD Flag from the loader
						delete window.define.amd;
					}
					bGlobalAsyncMode = bAsync;

					if ( bLoggable ) {
						log.debug(sLogPrefix + "executing '" + sModuleName + "'");
						sOldPrefix = sLogPrefix;
						sLogPrefix = sLogPrefix + ": ";
					}

					// execute the script in the window context
					oModule.state = EXECUTING;
					_execStack.push(sModuleName);
					if ( typeof oModule.data === "function" ) {
						callPreloadWrapperFn(oModule.data);
					} else if ( Array.isArray(oModule.data) ) {
						sap.ui.define.apply(sap.ui, oModule.data);
					} else {

						sScript = oModule.data;

						// sourceURL: Firebug, Chrome, Safari and IE11 debugging help, appending the string seems to cost ZERO performance
						// Note: IE11 supports sourceURL even when running in IE9 or IE10 mode
						// Note: make URL absolute so Chrome displays the file tree correctly
						// Note: do not append if there is already a sourceURL / sourceMappingURL
						// Note: Safari fails, if sourceURL is the same as an existing XHR URL
						// Note: Chrome ignores debug files when the same URL has already been load via sourcemap of the bootstrap file (sap-ui-core)
						// Note: sourcemap annotations URLs in eval'ed sources are resolved relative to the page, not relative to the source
						if (sScript ) {
							oMatch = /\/\/[#@] source(Mapping)?URL=(.*)$/.exec(sScript);
							if ( oMatch && oMatch[1] && /[^/]+\.js\.map$/.test(oMatch[2]) ) {
								// found a sourcemap annotation with a typical UI5 generated relative URL
								sScript = sScript.slice(0, oMatch.index) + oMatch[0].slice(0, -oMatch[2].length) + URI(oMatch[2]).absoluteTo(oModule.url);
							} else if ( !oMatch ) {
								sScript += "\n//# sourceURL=" + URI(oModule.url).absoluteTo(sDocumentLocation);
								if (Device.browser.safari || Device.browser.chrome) {
									sScript += "?eval";
								}
							}
						}

						// framework internal hook to intercept the loaded script and modify
						// it before executing the script - e.g. useful for client side coverage
						if (typeof jQuery.sap.require._hook === "function") {
							sScript = jQuery.sap.require._hook(sScript, sModuleName);
						}

						if (window.execScript && (!oModule.data || oModule.data.length < MAX_EXEC_SCRIPT_LENGTH) ) {
							try {
								oModule.data && window.execScript(sScript); // execScript fails if data is empty
							} catch (e) {
								_execStack.pop();
								// eval again with different approach - should fail with a more informative exception
								jQuery.sap.globalEval(oModule.data);
								throw e; // rethrow err in case globalEval succeeded unexpectedly
							}
						} else {
							evalModuleStr(sScript);
						}
					}
					_execStack.pop();
					oModule.state = READY;
					oModule.data = undefined;
					oModule.value(); // enforce determination of module value for non-AMD modules

					if ( bLoggable ) {
						sLogPrefix = sOldPrefix;
						log.debug(sLogPrefix + "finished executing '" + sModuleName + "'");
					}

				} catch (err) {
					oModule.state = FAILED;
					oModule.errorStack = err && err.stack;
					oModule.errorMessage = ((err.toString && err.toString()) || err.message) + (err.line ? "(line " + err.line + ")" : "" );
					oModule.data = undefined;
					if ( window["sap-ui-debug"] && (/sap-ui-xx-show(L|-l)oad(E|-e)rrors=(true|x|X)/.test(location.search) || oCfgData["xx-showloaderrors"]) ) {
						log.error("error while evaluating " + sModuleName + ", embedding again via script tag to enforce a stack trace (see below)");
						jQuery.sap.includeScript(oModule.url);
						return;
					}

				} finally {

					// restore AMD flag
					if ( vAMD ) {
						window.define.amd = vAMD;
					}
					bGlobalAsyncMode = bOldGlobalAsyncMode;
				}
			}
		}

		function requireAll(oRequestingModule, aDependencies, fnCallback, bAsync) {

			var aModules = [],
				bLoggable = log.isLoggable(),
				sBaseName, i, sDepModName;

			// calculate the base name for relative module names
			sBaseName = oRequestingModule && oRequestingModule.name.slice(0, oRequestingModule.name.lastIndexOf('/') + 1);
			aDependencies = aDependencies.slice();
			for (i = 0; i < aDependencies.length; i++) {
				aDependencies[i] = resolveModuleName(sBaseName, aDependencies[i]) + ".js";
			}

			for (i = 0; i < aDependencies.length; i++) {
				sDepModName = aDependencies[i];
				if ( bLoggable ) {
					log.debug(sLogPrefix + "require '" + sDepModName + "'");
				}
				aModules[i] = requireModule(oRequestingModule, sDepModName, bAsync);
				if ( bLoggable ) {
					log.debug(sLogPrefix + "require '" + sDepModName + "': done.");
				}
			}

			return fnCallback(aModules);
		}

		/**
		 * Constructs an URL to load the module with the given name and file type (suffix).
		 *
		 * Searches the longest prefix of the given module name for which a registration
		 * exists (see {@link jQuery.sap.registerModulePath}) and replaces that prefix
		 * by the registered URL prefix.
		 *
		 * The remainder of the module name is appended to the URL, replacing any dot with a slash.
		 *
		 * Finally, the given suffix (typically a file name extension) is added (unconverted).
		 *
		 * The returned name (without the suffix) doesn't end with a slash.
		 *
		 * @param {string} sModuleName module name to detemrine the path for
		 * @param {string} sSuffix suffix to be added to the resulting path
		 * @return {string} calculated path (URL) to the given module
		 *
		 * @public
		 * @static
		 */
		jQuery.sap.getModulePath = function(sModuleName, sSuffix) {
			return getResourcePath(ui5ToRJS(sModuleName), sSuffix);
		};

		/**
		 * Determines the URL for a resource given its unified resource name.
		 *
		 * Searches the longest prefix of the given resource name for which a registration
		 * exists (see {@link jQuery.sap.registerResourcePath}) and replaces that prefix
		 * by the registered URL prefix.
		 *
		 * The remainder of the resource name is appended to the URL.
		 *
		 * <b>Unified Resource Names</b><br>
		 * Several UI5 APIs use <i>Unified Resource Names (URNs)</i> as naming scheme for resources that
		 * they deal with (e.h. Javascript, CSS, JSON, XML, ...). URNs are similar to the path
		 * component of an URL:
		 * <ul>
		 * <li>they consist of a non-empty sequence of name segments</li>
		 * <li>segments are separated by a forward slash '/'</li>
		 * <li>name segments consist of URL path segment characters only. It is recommended to use only ASCII
		 * letters (upper or lower case), digits and the special characters '$', '_', '-', '.')</li>
		 * <li>the empty name segment is not supported</li>
		 * <li>names consisting of dots only, are reserved and must not be used for resources</li>
		 * <li>names are case sensitive although the underlying server might be case-insensitive</li>
		 * <li>the behavior with regard to URL encoded characters is not specified, %ddd notation should be avoided</li>
		 * <li>the meaning of a leading slash is undefined, but might be defined in future. It therefore should be avoided</li>
		 * </ul>
		 *
		 * UI5 APIs that only deal with Javascript resources, use a slight variation of this scheme,
		 * where the extension '.js' is always omitted (see {@link sap.ui.define}, {@link sap.ui.require}).
		 *
		 *
		 * <b>Relationship to old Module Name Syntax</b><br>
		 *
		 * Older UI5 APIs that deal with resources (like {@link jQuery.sap.registerModulePath},
		 * {@link jQuery.sap.require} and {@link jQuery.sap.declare}) used a dot-separated naming scheme
		 * (called 'module names') which was motivated by object names in the global namespace in
		 * Javascript.
		 *
		 * The new URN scheme better matches the names of the corresponding resources (files) as stored
		 * in a server and the dot ('.') is no longer a forbidden character in a resource name. This finally
		 * allows to handle resources with different types (extensions) with the same API, not only JS files.
		 *
		 * Last but not least does the URN scheme better match the naming conventions used by AMD loaders
		 * (like <code>requireJS</code>).
		 *
		 * @param {string} sResourceName unified resource name of the resource
		 * @returns {string} URL to load the resource from
		 * @public
		 * @experimental Since 1.27.0
		 * @function
		 */
		jQuery.sap.getResourcePath = getResourcePath;

		/**
		 * Registers an URL prefix for a module name prefix.
		 *
		 * Before a module is loaded, the longest registered prefix of its module name
		 * is searched for and the associated URL prefix is used as a prefix for the request URL.
		 * The remainder of the module name is attached to the request URL by replacing
		 * dots ('.') with slashes ('/').
		 *
		 * The registration and search operates on full name segments only. So when a prefix
		 *
		 *    'sap.com'  ->  'http://www.sap.com/ui5/resources/'
		 *
		 * is registered, then it will match the name
		 *
		 *    'sap.com.Button'
		 *
		 * but not
		 *
		 *    'sap.commons.Button'
		 *
		 * Note that the empty prefix ('') will always match and thus serves as a fallback for
		 * any search.
		 *
		 * The prefix can either be given as string or as object which contains the url and a 'final' property.
		 * If 'final' is set to true, overwriting a module prefix is not possible anymore.
		 *
		 * @param {string} sModuleName module name to register a path for
		 * @param {string | object} vUrlPrefix path prefix to register, either a string literal or an object (e.g. {url : 'url/to/res', 'final': true})
		 * @param {string} [vUrlPrefix.url] path prefix to register
		 * @param {boolean} [vUrlPrefix.final] flag to avoid overwriting the url path prefix for the given module name at a later point of time
		 *
		 * @public
		 * @static
		 * @SecSink {1|PATH} Parameter is used for future HTTP requests
		 */
		jQuery.sap.registerModulePath = function registerModulePath(sModuleName, vUrlPrefix) {
			jQuery.sap.assert(!/\//.test(sModuleName), "module path must not contain a slash.");
			sModuleName = sModuleName.replace(/\./g, "/");
			// URL must not be empty
			vUrlPrefix = vUrlPrefix || '.';
			jQuery.sap.registerResourcePath(sModuleName, vUrlPrefix);
		};

		/**
		 * Registers an URL prefix for a resource name prefix.
		 *
		 * Before a resource is loaded, the longest registered prefix of its unified resource name
		 * is searched for and the associated URL prefix is used as a prefix for the request URL.
		 * The remainder of the resource name is attached to the request URL 1:1.
		 *
		 * The registration and search operates on full name segments only. So when a prefix
		 *
		 *    'sap/com'  ->  'http://www.sap.com/ui5/resources/'
		 *
		 * is registered, then it will match the name
		 *
		 *    'sap/com/Button'
		 *
		 * but not
		 *
		 *    'sap/commons/Button'
		 *
		 * Note that the empty prefix ('') will always match and thus serves as a fallback for
		 * any search.
		 *
		 * The url prefix can either be given as string or as object which contains the url and a final flag.
		 * If final is set to true, overwriting a resource name prefix is not possible anymore.
		 *
		 * @param {string} sResourceNamePrefix in unified resource name syntax
		 * @param {string | object} vUrlPrefix prefix to use instead of the sResourceNamePrefix, either a string literal or an object (e.g. {url : 'url/to/res', 'final': true})
		 * @param {string} [vUrlPrefix.url] path prefix to register
		 * @param {boolean} [vUrlPrefix.final] flag to avoid overwriting the url path prefix for the given module name at a later point of time
		 *
		 * @public
		 * @static
		 * @SecSink {1|PATH} Parameter is used for future HTTP requests
		 */
		jQuery.sap.registerResourcePath = function registerResourcePath(sResourceNamePrefix, vUrlPrefix) {

			function same(oPrefix1, oPrefix2) {
				return oPrefix1.url === oPrefix2.url && !oPrefix1["final"] === !oPrefix2["final"];
			}

			sResourceNamePrefix = String(sResourceNamePrefix || "");

			if ( typeof vUrlPrefix === 'string' || vUrlPrefix instanceof String ) {
				vUrlPrefix = { 'url' : vUrlPrefix };
			}

			var oOldPrefix = mUrlPrefixes[sResourceNamePrefix];

			if (oOldPrefix && oOldPrefix["final"] == true) {
				if ( !vUrlPrefix || !same(oOldPrefix, vUrlPrefix) ) {
					log.warning( "registerResourcePath with prefix " + sResourceNamePrefix + " already set as final to '" + oOldPrefix.url + "'. This call is ignored." );
				}
				return;
			}

			if ( !vUrlPrefix || vUrlPrefix.url == null ) {

				if ( oOldPrefix ) {
					delete mUrlPrefixes[sResourceNamePrefix];
					log.info("registerResourcePath ('" + sResourceNamePrefix + "') (registration removed)");
				}

			} else {

				vUrlPrefix.url = String(vUrlPrefix.url);

				// remove query parameters and/or hash
				var iQueryOrHashIndex = vUrlPrefix.url.search(/[?#]/);
				if (iQueryOrHashIndex !== -1) {
					vUrlPrefix.url = vUrlPrefix.url.slice(0, iQueryOrHashIndex);
				}

				// ensure that the prefix ends with a '/'
				if ( vUrlPrefix.url.slice(-1) != '/' ) {
					vUrlPrefix.url += '/';
				}

				mUrlPrefixes[sResourceNamePrefix] = vUrlPrefix;

				if ( !oOldPrefix || !same(oOldPrefix, vUrlPrefix) ) {
					log.info("registerResourcePath ('" + sResourceNamePrefix + "', '" + vUrlPrefix.url + "')" + (vUrlPrefix['final'] ? " (final)" : ""));
				}
			}
		};

		/**
		 * Register information about third party modules that are not UI5 modules.
		 *
		 * The information maps the name of the module (without extension '.js') to an info object.
		 * Instead of a complete info object, only the value of the <code>deps</code> property can be given as an array.
		 *
		 * @param {object} mShims Map of shim configuration objects keyed by module names (withou extension '.js')
		 * @param {boolean} [mShims.any-module-name.amd=false]
		 *              Whether the module uses an AMD loader if present. If set to <code>true</code>, UI5 will disable
		 *              the AMD loader while loading such modules to force the modules to expose their content via global names.
		 * @param {string[]|string} [mShims.any-module-name.exports=undefined]
		 *              Global name (or names) that are exported by the module. If one ore multiple names are defined,
		 *              the first one will be read from the global object and will be used as value of the module.
		 *              Each name can be a dot separated hierarchial name (will be resolved with <code>jQuery.sap.getObject</code>)
		 * @param {string[]} [mShims.any-module-name.deps=undefined]
		 *              List of modules that the module depends on (requireJS syntax, no '.js').
		 *              The modules will be loaded first before loading the module itself.
		 *
		 * @private
		 */
		jQuery.sap.registerModuleShims = function(mShims) {
			jQuery.sap.assert( typeof mShims === 'object', "mShims must be an object");

			for ( var sName in mShims ) {
				var oShim = mShims[sName];
				if ( Array.isArray(oShim) ) {
					oShim = { deps : oShim };
				}
				mAMDShim[sName + ".js"] = oShim;
			}
		};

		/**
		 * Check whether a given module has been loaded / declared already.
		 *
		 * Returns true as soon as a module has been required the first time, even when
		 * loading/executing it has not finished yet. So the main assertion of a
		 * return value of <code>true</code> is that the necessary actions have been taken
		 * to make the module available in the near future. It does not mean, that
		 * the content of the module is already available!
		 *
		 * This fuzzy behavior is necessary to avoid multiple requests for the same module.
		 * As a consequence of the assertion above, a <i>preloaded</i> module does not
		 * count as <i>declared</i>. For preloaded modules, an explicit call to
		 * <code>jQuery.sap.require</code> is necessary to make them available.
		 *
		 * If a caller wants to know whether a module needs to be loaded from the server,
		 * it can set <code>bIncludePreloaded</code> to true. Then, preloaded modules will
		 * be reported as 'declared' as well by this method.
		 *
		 * @param {string} sModuleName name of the module to be checked
		 * @param {boolean} [bIncludePreloaded=false] whether preloaded modules should be reported as declared.
		 * @return {boolean} whether the module has been declared already
		 * @public
		 * @static
		 */
		jQuery.sap.isDeclared = function isDeclared(sModuleName, bIncludePreloaded) {
			sModuleName = ui5ToRJS(sModuleName) + ".js";
			return mModules[sModuleName] && (bIncludePreloaded || mModules[sModuleName].state !== PRELOADED);
		};

		/**
		 * Whether the given resource has been loaded (or preloaded).
		 * @param {string} sResourceName Name of the resource to check, in unified resource name format
		 * @returns {boolean} Whether the resource has been loaded already
		 * @private
		 * @sap-restricted sap.ui.core
		 */
		jQuery.sap.isResourceLoaded = function isResourceLoaded(sResourceName) {
			return mModules[sResourceName];
		};

		/**
		 * Returns the names of all declared modules.
		 * @return {string[]} the names of all declared modules
		 * @see jQuery.sap.isDeclared
		 * @public
		 * @static
		 */
		jQuery.sap.getAllDeclaredModules = function() {
			var aModules = [];
			jQuery.each(mModules, function(sURN, oModule) {
				// filter out preloaded modules
				if ( oModule && oModule.state !== PRELOADED ) {
					var sModuleName = urnToUI5(sURN);
					if ( sModuleName ) {
						aModules.push(sModuleName);
					}
				}
			});
			return aModules;
		};

		// take resource roots from configuration
		if ( oCfgData.resourceroots ) {
			jQuery.each(oCfgData.resourceroots, jQuery.sap.registerModulePath);
		}

		// dump the URL prefixes
		log.info("URL prefixes set to:");
		for (var n in mUrlPrefixes) {
			log.info("  " + (n ? "'" + n + "'" : "(default)") + " : " + mUrlPrefixes[n].url + ((mUrlPrefixes[n]['final']) ? " (final)" : "") );
		}

		/**
		 * Declares a module as existing.
		 *
		 * By default, this function assumes that the module will create a JavaScript object
		 * with the same name as the module. As a convenience it ensures that the parent
		 * namespace for that object exists (by calling jQuery.sap.getObject).
		 * If such an object creation is not desired, <code>bCreateNamespace</code> must be set to false.
		 *
		 * @param {string | object}  sModuleName name of the module to be declared
		 *                           or in case of an object {modName: "...", type: "..."}
		 *                           where modName is the name of the module and the type
		 *                           could be a specific dot separated extension e.g.
		 *                           <code>{modName: "sap.ui.core.Dev", type: "view"}</code>
		 *                           loads <code>sap/ui/core/Dev.view.js</code> and
		 *                           registers as <code>sap.ui.core.Dev.view</code>
		 * @param {boolean} [bCreateNamespace=true] whether to create the parent namespace
		 *
		 * @public
		 * @static
		 */
		jQuery.sap.declare = function(sModuleName, bCreateNamespace) {

			var sNamespaceObj = sModuleName;

			// check for an object as parameter for sModuleName
			// in case of this the object contains the module name and the type
			// which could be {modName: "sap.ui.core.Dev", type: "view"}
			if (typeof (sModuleName) === "object") {
				sNamespaceObj = sModuleName.modName;
				sModuleName = ui5ToRJS(sModuleName.modName) + (sModuleName.type ? "." + sModuleName.type : "") + ".js";
			} else {
				sModuleName = ui5ToRJS(sModuleName) + ".js";
			}

			declareModule(sModuleName);

			// ensure parent namespace even if module was declared already
			// (as declare might have been called by require)
			if (bCreateNamespace !== false) {
				// ensure parent namespace
				jQuery.sap.getObject(sNamespaceObj, 1);
			}

		};

		/**
		 * Ensures that the given module is loaded and executed before execution of the
		 * current script continues.
		 *
		 * By issuing a call to this method, the caller declares a dependency to the listed modules.
		 *
		 * Any required and not yet loaded script will be loaded and execute synchronously.
		 * Already loaded modules will be skipped.
		 *
		 * @param {...string | object}  vModuleName one or more names of modules to be loaded
		 *                              or in case of an object {modName: "...", type: "..."}
		 *                              where modName is the name of the module and the type
		 *                              could be a specific dot separated extension e.g.
		 *                              <code>{modName: "sap.ui.core.Dev", type: "view"}</code>
		 *                              loads <code>sap/ui/core/Dev.view.js</code> and
		 *                              registers as <code>sap.ui.core.Dev.view</code>
		 *
		 * @public
		 * @static
		 * @function
		 * @SecSink {0|PATH} Parameter is used for future HTTP requests
		 */
		jQuery.sap.require = function(vModuleName) {

			if ( arguments.length > 1 ) {
				// legacy mode with multiple arguments, each representing a dependency
				for (var i = 0; i < arguments.length; i++) {
					jQuery.sap.require(arguments[i]);
				}
				return this;
			}

			// check for an object as parameter for sModuleName
			// in case of this the object contains the module name and the type
			// which could be {modName: "sap.ui.core.Dev", type: "view"}
			if (typeof (vModuleName) === "object") {
				jQuery.sap.assert(!vModuleName.type || mKnownSubtypes.js.indexOf(vModuleName.type) >= 0, "type must be empty or one of " + mKnownSubtypes.js.join(", "));
				vModuleName = ui5ToRJS(vModuleName.modName) + (vModuleName.type ? "." + vModuleName.type : "") + ".js";
			} else {
				vModuleName = ui5ToRJS(vModuleName) + ".js";
			}

			requireModule(null, vModuleName, /* bAsync = */ false);

		};

		window.sap = window.sap || {};
		sap.ui = sap.ui || {};

		/**
		 * Defines a Javascript module with its name, its dependencies and a module value or factory.
		 *
		 * The typical and only suggested usage of this method is to have one single, top level call to
		 * <code>sap.ui.define</code> in one Javascript resource (file). When a module is requested by its
		 * name for the first time, the corresponding resource is determined from the name and the current
		 * {@link jQuery.sap.registerResourcePath configuration}. The resource will be loaded and executed
		 * which in turn will execute the top level <code>sap.ui.define</code> call.
		 *
		 * If the module name was omitted from that call, it will be substituted by the name that was used to
		 * request the module. As a preparation step, the dependencies as well as their transitive dependencies,
		 * will be loaded. Then, the module value will be determined: if a static value (object, literal) was
		 * given as <code>vFactory</code>, that value will be the module value. If a function was given, that
		 * function will be called (providing the module values of the declared dependencies as parameters
		 * to the function) and its return value will be used as module value. The framework internally associates
		 * the resulting value with the module name and provides it to the original requester of the module.
		 * Whenever the module is requested again, the same value will be returned (modules are executed only once).
		 *
		 * <i>Example:</i><br>
		 * The following example defines a module "SomeClass", but doesn't hard code the module name.
		 * If stored in a file 'sap/mylib/SomeClass.js', it can be requested as 'sap/mylib/SomeClass'.
		 * <pre>
		 *   sap.ui.define(['./Helper', 'sap/m/Bar'], function(Helper,Bar) {
		 *
		 *     // create a new class
		 *     var SomeClass = function() {};
		 *
		 *     // add methods to its prototype
		 *     SomeClass.prototype.foo = function() {
		 *
		 *         // use a function from the dependency 'Helper' in the same package (e.g. 'sap/mylib/Helper' )
		 *         var mSettings = Helper.foo();
		 *
		 *         // create and return a sap.m.Bar (using its local name 'Bar')
		 *         return new Bar(mSettings);
		 *
		 *     }
		 *
		 *     // return the class as module value
		 *     return SomeClass;
		 *
		 *   });
		 * </pre>
		 *
		 * In another module or in an application HTML page, the {@link sap.ui.require} API can be used
		 * to load the Something module and to work with it:
		 *
		 * <pre>
		 * sap.ui.require(['sap/mylib/Something'], function(Something) {
		 *
		 *   // instantiate a Something and call foo() on it
		 *   new Something().foo();
		 *
		 * });
		 * </pre>
		 *
		 * <b>Module Name Syntax</b><br>
		 * <code>sap.ui.define</code> uses a simplified variant of the {@link jQuery.sap.getResourcePath
		 * unified resource name} syntax for the module's own name as well as for its dependencies.
		 * The only difference to that syntax is, that for <code>sap.ui.define</code> and
		 * <code>sap.ui.require</code>, the extension (which always would be '.js') has to be omitted.
		 * Both methods always add this extension internally.
		 *
		 * As a convenience, the name of a dependency can start with the segment './' which will be
		 * replaced by the name of the package that contains the currently defined module (relative name).
		 *
		 * It is best practice to omit the name of the defined module (first parameter) and to use
		 * relative names for the dependencies whenever possible. This reduces the necessary configuration,
		 * simplifies renaming of packages and allows to map them to a different namespace.
		 *
		 *
		 * <b>Dependency to Modules</b><br>
		 * If a dependencies array is given, each entry represents the name of another module that
		 * the currently defined module depends on. All dependency modules are loaded before the value
		 * of the currently defined module is determined. The module value of each dependency module
		 * will be provided as a parameter to a factory function, the order of the parameters will match
		 * the order of the modules in the dependencies array.
		 *
		 * <b>Note:</b> the order in which the dependency modules are <i>executed</i> is <b>not</b>
		 * defined by the order in the dependencies array! The execution order is affected by dependencies
		 * <i>between</i> the dependency modules as well as by their current state (whether a module
		 * already has been loaded or not). Neither module implementations nor dependents that require
		 * a module set must make any assumption about the execution order (other than expressed by
		 * their dependencies). There is, however, one exception with regard to third party libraries,
		 * see the list of limitations further down below.
		 *
		 * <b>Note:</b>a static module value (a literal provided to <code>sap.ui.define</code>) cannot
		 * depend on the module values of the dependency modules. Instead, modules can use a factory function,
		 * calculate the static value in that function, potentially based on the dependencies, and return
		 * the result as module value. The same approach must be taken when the module value is supposed
		 * to be a function.
		 *
		 *
		 * <b>Asynchronous Contract</b><br>
		 * <code>sap.ui.define</code> is designed to support real Asynchronous Module Definitions (AMD)
		 * in future, although it internally still uses the the old synchronous module loading of UI5.
		 * Callers of <code>sap.ui.define</code> therefore must not rely on any synchronous behavior
		 * that they might observe with the current implementation.
		 *
		 * For example, callers of <code>sap.ui.define</code> must not use the module value immediately
		 * after invoking <code>sap.ui.define</code>:
		 *
		 * <pre>
		 *   // COUNTER EXAMPLE HOW __NOT__ TO DO IT
		 *
		 *   // define a class Something as AMD module
		 *   sap.ui.define('Something', [], function() {
		 *     var Something = function() {};
		 *     return Something;
		 *   });
		 *
		 *   // DON'T DO THAT!
		 *   // accessing the class _synchronously_ after sap.ui.define was called
		 *   new Something();
		 * </pre>
		 *
		 * Applications that need to ensure synchronous module definition or synchronous loading of dependencies
		 * <b>MUST</b> use the old {@link jQuery.sap.declare} and {@link jQuery.sap.require} APIs.
		 *
		 *
		 * <b>(No) Global References</b><br>
		 * To be in line with AMD best practices, modules defined with <code>sap.ui.define</code>
		 * should not make any use of global variables if those variables are also available as module
		 * values. Instead, they should add dependencies to those modules and use the corresponding parameter
		 * of the factory function to access the module value.
		 *
		 * As the current programming model and the documentation of UI5 heavily rely on global names,
		 * there will be a transition phase where UI5 enables AMD modules and local references to module
		 * values in parallel to the old global names. The fourth parameter of <code>sap.ui.define</code>
		 * has been added to support that transition phase. When this parameter is set to true, the framework
		 * provides two additional functionalities
		 *
		 * <ol>
		 * <li>before the factory function is called, the existence of the global parent namespace for
		 *     the current module is ensured</li>
		 * <li>the module value will be automatically exported under a global name which is derived from
		 *     the name of the module</li>
		 * </ol>
		 *
		 * The parameter lets the framework know whether any of those two operations is needed or not.
		 * In future versions of UI5, a central configuration option is planned to suppress those 'exports'.
		 *
		 *
		 * <b>Third Party Modules</b><br>
		 * Although third party modules don't use UI5 APIs, they still can be listed as dependencies in
		 * a <code>sap.ui.define</code> call. They will be requested and executed like UI5 modules, but their
		 * module value will be <code>undefined</code>.
		 *
		 * If the currently defined module needs to access the module value of such a third party module,
		 * it can access the value via its global name (if the module supports such a usage).
		 *
		 * Note that UI5 temporarily deactivates an existing AMD loader while it executes third party modules
		 * known to support AMD. This sounds contradictorily at a first glance as UI5 wants to support AMD,
		 * but for now it is necessary to fully support UI5 applications that rely on global names for such modules.
		 *
		 * Example:
		 * <pre>
		 *   // module 'Something' wants to use third party library 'URI.js'
		 *   // It is packaged by UI5 as non-UI5-module 'sap/ui/thirdparty/URI'
		 *
		 *   sap.ui.define('Something', ['sap/ui/thirdparty/URI'], function(URIModuleValue) {
		 *
		 *     new URIModuleValue(); // fails as module value is undefined
		 *
		 *     //global URI // (optional) declare usage of global name so that static code checks don't complain
		 *     new URI(); // access to global name 'URI' works
		 *
		 *     ...
		 *   });
		 * </pre>
		 *
		 *
		 * <b>Differences to requireJS</b><br>
		 * The current implementation of <code>sap.ui.define</code> differs from <code>requireJS</code>
		 * or other AMD loaders in several aspects:
		 * <ul>
		 * <li>the name <code>sap.ui.define</code> is different from the plain <code>define</code>.
		 * This has two reasons: first, it avoids the impression that <code>sap.ui.define</code> is
		 * an exact implementation of an AMD loader. And second, it allows the coexistence of an AMD
		 * loader (requireJS) and <code>sap.ui.define</code> in one application as long as UI5 or
		 * applications using UI5 are not fully prepared to run with an AMD loader</li>
		 * <li><code>sap.ui.define</code> currently loads modules with synchronous XHR calls. This is
		 * basically a tribute to the synchronous history of UI5.
		 * <b>BUT:</b> synchronous dependency loading and factory execution explicitly it not part of
		 * contract of <code>sap.ui.define</code>. To the contrary, it is already clear and planned
		 * that asynchronous loading will be implemented, at least as an alternative if not as the only
		 * implementation. Also check section <b>Asynchronous Contract</b> above.<br>
		 * Applications that need to ensure synchronous loading of dependencies <b>MUST</b> use the old
		 * {@link jQuery.sap.require} API.</li>
		 * <li><code>sap.ui.define</code> does not support plugins to use other file types, formats or
		 * protocols. It is not planned to support this in future</li>
		 * <li><code>sap.ui.define</code> does <b>not</b> support the 'sugar' of requireJS where CommonJS
		 * style dependency declarations using <code>sap.ui.require("something")</code> are automagically
		 * converted into <code>sap.ui.define</code> dependencies before executing the factory function.</li>
		 * </ul>
		 *
		 *
		 * <b>Limitations, Design Considerations</b><br>
		 * <ul>
		 * <li><b>Limitation</b>: as dependency management is not supported for Non-UI5 modules, the only way
		 *     to ensure proper execution order for such modules currently is to rely on the order in the
		 *     dependency array. Obviously, this only works as long as <code>sap.ui.define</code> uses
		 *     synchronous loading. It will be enhanced when asynchronous loading is implemented.</li>
		 * <li>it was discussed to enforce asynchronous execution of the module factory function (e.g. with a
		 *     timeout of 0). But this would have invalidated the current migration scenario where a
		 *     sync <code>jQuery.sap.require</code> call can load a <code>sap.ui.define</code>'ed module.
		 *     If the module definition would not execute synchronously, the synchronous contract of the
		 *     require call would be broken (default behavior in existing UI5 applications)</li>
		 * <li>a single file must not contain multiple calls to <code>sap.ui.define</code>. Multiple calls
		 *     currently are only supported in the so called 'preload' files that the UI5 merge tooling produces.
		 *     The exact details of how this works might be changed in future implementations and are not
		 *     yet part of the API contract</li>
		 * </ul>
		 * @param {string} [sModuleName] name of the module in simplified resource name syntax.
		 *        When omitted, the loader determines the name from the request.
		 * @param {string[]} [aDependencies] list of dependencies of the module
		 * @param {function|any} vFactory the module value or a function that calculates the value
		 * @param {boolean} [bExport] whether an export to global names is required - should be used by SAP-owned code only
		 * @since 1.27.0
		 * @public
		 * @experimental Since 1.27.0 - not all aspects of sap.ui.define are settled yet. If the documented
		 *        constraints and limitations are obeyed, SAP-owned code might use it. If the fourth parameter
		 *        is not used and if the asynchronous contract is respected, even Non-SAP code might use it.
		 */
		sap.ui.define = function(sModuleName, aDependencies, vFactory, bExport) {
			var bLoggable = log.isLoggable(),
				sResourceName;

			// optional id
			if ( typeof sModuleName === 'string' ) {
				sResourceName = sModuleName + '.js';
			} else {
				// shift parameters
				bExport = vFactory;
				vFactory = aDependencies;
				aDependencies = sModuleName;
				sResourceName = _execStack[_execStack.length - 1];
			}

			// convert module name to UI5 module name syntax (might fail!)
			sModuleName = urnToUI5(sResourceName);

			// optional array of dependencies
			if ( !Array.isArray(aDependencies) ) {
				// shift parameters
				bExport = vFactory;
				vFactory = aDependencies;
				aDependencies = [];
			}

			if ( bLoggable ) {
				log.debug("define(" + sResourceName + ", " + "['" + aDependencies.join("','") + "']" + ")");
			}

			var oModule = declareModule(sResourceName);
			// avoid early evaluation of the module value
			oModule.content = undefined;

			// Note: dependencies will be resolved and converted from RJS to URN inside requireAll
			requireAll(oModule, aDependencies, function(aModules) {

				// factory
				if ( bLoggable ) {
					log.debug("define(" + sResourceName + "): calling factory " + typeof vFactory);
				}

				if ( bExport && syncCallBehavior !== 2 ) {
					// ensure parent namespace
					var sPackage = sResourceName.split('/').slice(0,-1).join('.');
					if ( sPackage ) {
						jQuery.sap.getObject(sPackage, 0);
					}
				}

				if ( typeof vFactory === 'function' ) {
					oModule.content = applyAMDFactoryFn(vFactory, aModules);
				} else {
					oModule.content = vFactory;
				}

				// HACK: global export
				if ( bExport && syncCallBehavior !== 2 ) {
					if ( oModule.content == null ) {
						log.error("module '" + sResourceName + "' returned no content, but should be exported");
					} else {
						if ( bLoggable ) {
							log.debug("exporting content of '" + sResourceName + "': as global object");
						}
						jQuery.sap.setObject(sModuleName, oModule.content);
					}
				}

			}, /* bAsync = */ bGlobalAsyncMode);

		};

		/**
		 * @private
		 */
		sap.ui.predefine = function(sModuleName, aDependencies, vFactory, bExport) {

			if ( typeof sModuleName !== 'string' ) {
				throw new Error("sap.ui.predefine requires a module name");
			}

			var sResourceName = sModuleName + '.js';
			Module.get(sResourceName).preload("<unknown>/" + sModuleName, [sModuleName, aDependencies, vFactory, bExport], null);

			// when a library file is preloaded, also mark its preload file as loaded
			// for normal library preload, this is redundant, but for non-default merged entities
			// like sap/fiori/core.js it avoids redundant loading of library preload files
			if ( sResourceName.match(/\/library\.js$/) ) {
				mPreloadModules[urnToUI5(sResourceName) + "-preload"] = true;
			}

		};

		/**
		 * Resolves one or more module dependencies.
		 *
		 * <b>Synchronous Retrieval of a Single Module Value</b>
		 *
		 * When called with a single string, that string is assumed to be the name of an already loaded
		 * module and the value of that module is returned. If the module has not been loaded yet,
		 * or if it is a Non-UI5 module (e.g. third party module), <code>undefined</code> is returned.
		 * This signature variant allows synchronous access to module values without initiating module loading.
		 *
		 * Sample:
		 * <pre>
		 *   var JSONModel = sap.ui.require("sap/ui/model/json/JSONModel");
 		 * </pre>
 		 *
 		 * For modules that are known to be UI5 modules, this signature variant can be used to check whether
 		 * the module has been loaded.
 		 *
		 * <b>Asynchronous Loading of Multiple Modules</b>
		 *
		 * If an array of strings is given and (optionally) a callback function, then the strings
		 * are interpreted as module names and the corresponding modules (and their transitive
		 * dependencies) are loaded. Then the callback function will be called asynchronously.
		 * The module values of the specified modules will be provided as parameters to the callback
		 * function in the same order in which they appeared in the dependencies array.
		 *
		 * The return value for the asynchronous use case is <code>undefined</code>.
		 *
		 * <pre>
		 *   sap.ui.require(['sap/ui/model/json/JSONModel', 'sap/ui/core/UIComponent'], function(JSONModel,UIComponent) {
		 *
		 *     var MyComponent = UIComponent.extend('MyComponent', {
		 *       ...
		 *     });
		 *     ...
		 *
		 *   });
 		 * </pre>
 		 *
		 * This method uses the same variation of the {@link jQuery.sap.getResourcePath unified resource name}
		 * syntax that {@link sap.ui.define} uses: module names are specified without the implicit extension '.js'.
		 * Relative module names are not supported.
		 *
		 * @param {string|string[]} vDependencies dependency (dependencies) to resolve
		 * @param {function} [fnCallback] callback function to execute after resolving an array of dependencies
		 * @returns {any|undefined} a single module value or undefined
		 * @public
		 * @experimental Since 1.27.0 - not all aspects of sap.ui.require are settled yet. E.g. the return value
		 * of the asynchronous use case might change (currently it is undefined).
		 */
		sap.ui.require = function(vDependencies, fnCallback) {
			jQuery.sap.assert(typeof vDependencies === 'string' || Array.isArray(vDependencies), "dependency param either must be a single string or an array of strings");
			jQuery.sap.assert(fnCallback == null || typeof fnCallback === 'function', "callback must be a function or null/undefined");

			if ( typeof vDependencies === 'string' ) {

				return Module.get(vDependencies + '.js').value();

			}

			requireAll(null, vDependencies, function(aModules) {

				if ( typeof fnCallback === 'function' ) {
					// enforce asynchronous execution of callback
					setTimeout(function() {
						fnCallback.apply(window, aModules);
					},0);
				}

			}, /* bAsync = */ true);

			// return undefined;
		};

		/**
		 * @private
		 */
		sap.ui.require.stat = function(iState) {
			var i = 0;
			Object.keys(mModules).sort().forEach(function(sModule) {
				if ( mModules[sModule].state >= iState ) {
					log.info( (++i) + " " + sModule + " " + mModules[sModule].state);
				}
			});
			log.info("apply AMD factory function: #" + applyAMDFactoryFn.count);
			log.info("call preload wrapper function: #" + callPreloadWrapperFn.count);
			log.info("eval module string : #" + evalModuleStr.count);
		};

		/**
		 * Load a single module synchronously and return its module value.
		 *
		 * Basically, this method is a combination of {@link jQuery.sap.require} and {@link sap.ui.require}.
		 * Its main purpose is to simplify the migration of modules to AMD style in those cases where some dependencies
		 * have to be loaded late (lazy) and synchronously.
		 *
		 * The method accepts a single module name in the same syntax that {@link sap.ui.define} and {@link sap.ui.require}
		 * already use (a simplified variation of the {@link jQuery.sap.getResourcePath unified resource name}:
		 * slash separated names without the implicit extension '.js'). As for <code>sap.ui.require</code>,
		 * relative names (using <code>./</code> or <code>../</code>) are not supported.
		 * If not loaded yet, the named module will be loaded synchronously and the value of the module will be returned.
		 * While a module is executing, a value of <code>undefined</code> will be returned in case it is required again during
		 * that period of time.
		 *
		 * <b>Note</b>: Applications are strongly encouraged to use this method only when synchronous loading is unavoidable.
		 * Any code that uses this method won't benefit from future performance improvements that require asynchronous
		 * module loading. And such code never can comply with stronger content security policies (CSPs) that forbid 'eval'.
		 *
		 * @param {string} sModuleName Module name in requireJS syntax
		 * @returns {any} value of the loaded module or undefined
		 * @private
		 */
		sap.ui.requireSync = function(sModuleName) {
			return requireModule(null, sModuleName + ".js", /* bAsync = */ false);
		};

		/**
		 * @private
		 * @deprecated
		 */
		jQuery.sap.preloadModules = function(sPreloadModule, bAsync, oSyncPoint) {

			var sURL, iTask, sMsg;

			jQuery.sap.log.error("[Deprecated] jQuery.sap.preloadModules was never a public API and will be removed soon. Migrate to Core.loadLibraries()!");

			jQuery.sap.assert(!bAsync || oSyncPoint, "if mode is async, a syncpoint object must be given");

			if ( !bAsync && syncCallBehavior ) {
				sMsg = "[nosync] synchronous preload of '" + sPreloadModule + "'";
				if ( syncCallBehavior === 1 ) {
					log.warning(sMsg);
				} else {
					throw new Error(sMsg);
				}
			}

			if ( mPreloadModules[sPreloadModule] ) {
				return;
			}

			mPreloadModules[sPreloadModule] = true;

			sURL = jQuery.sap.getModulePath(sPreloadModule, ".json");

			log.debug("preload file " + sPreloadModule);
			iTask = oSyncPoint && oSyncPoint.startTask("load " + sPreloadModule);

			jQuery.ajax({
				dataType : "json",
				async : bAsync,
				url : sURL,
				success : function(data) {
					if ( data ) {
						jQuery.sap.registerPreloadedModules(data, sURL);
						// also preload dependencies
						if ( Array.isArray(data.dependencies) ) {
							data.dependencies.forEach(function(sDependency) {
								jQuery.sap.preloadModules(sDependency, bAsync, oSyncPoint);
							});
						}
					}
					oSyncPoint && oSyncPoint.finishTask(iTask);
				},
				error : function(xhr, textStatus, error) {
					log.error("failed to preload '" + sPreloadModule + "': " + (error || textStatus));
					oSyncPoint && oSyncPoint.finishTask(iTask, false);
				}
			});

		};

		/**
		 * Adds all resources from a preload bundle to the preload cache.
		 *
		 * When a resource exists already in the cache, the new content is ignored.
		 *
		 * @param {object} oData Preload bundle
		 * @param {string} [oData.url] URL from which the bundle has been loaded
		 * @param {string} [oData.name] Unique name of the bundle
		 * @param {string} [oData.version='1.0'] Format version of the preload bundle
		 * @param {object} oData.modules Map of resources keyed by their resource name; each resource must be a string or a function
		 *
		 * @private
		 * @sap-restricted sap.ui.core,preloadfiles
		 */
		jQuery.sap.registerPreloadedModules = function(oData) {

			var bOldSyntax = Version(oData.version || "1.0").compareTo("2.0") < 0;

			if ( log.isLoggable() ) {
				log.debug(sLogPrefix + "adding preloaded modules from '" + oData.url + "'");
			}

			if ( oData.name ) {
				mPreloadModules[oData.name] = true;
			}

			jQuery.each(oData.modules, function(sName, sContent) {
				sName = bOldSyntax ? ui5ToRJS(sName) + ".js" : sName;
				Module.get(sName).preload(oData.url + "/" + sName, sContent, oData.name);
				// when a library file is preloaded, also mark its preload file as loaded
				// for normal library preload, this is redundant, but for non-default merged entities
				// like sap/fiori/core.js it avoids redundant loading of library preload files
				if ( sName.match(/\/library\.js$/) ) {
					mPreloadModules[urnToUI5(sName) + "-preload"] = true;
				}
			});

		};

		/**
		 * Removes a set of resources from the resource cache.
		 *
		 * @param {string} sName unified resource name of a resource or the name of a preload group to be removed
		 * @param {boolean} [bPreloadGroup=true] whether the name specifies a preload group, defaults to true
		 * @param {boolean} [bUnloadAll] Whether all matching resources should be unloaded, even if they have been executed already.
		 * @param {boolean} [bDeleteExports] Whether exports (global variables) should be destroyed as well. Will be done for UI5 module names only.
		 * @experimental Since 1.16.3 API might change completely, apps must not develop against it.
		 * @private
		 */
		jQuery.sap.unloadResources = function(sName, bPreloadGroup, bUnloadAll, bDeleteExports) {
			var aModules = [];

			if ( bPreloadGroup == null ) {
				bPreloadGroup = true;
			}

			if ( bPreloadGroup ) {
				// collect modules that belong to the given group
				jQuery.each(mModules, function(sURN, oModule) {
					if ( oModule && oModule.group === sName ) {
						aModules.push(sURN);
					}
				});
				// also remove a preload entry
				delete mPreloadModules[sName];

			} else {
				// single module
				if ( mModules[sName] ) {
					aModules.push(sName);
				}
			}

			jQuery.each(aModules, function(i, sURN) {
				var oModule = mModules[sURN];
				if ( oModule && bDeleteExports && sURN.match(/\.js$/) ) {
					jQuery.sap.setObject(urnToUI5(sURN), undefined); // TODO really delete property
				}
				if ( oModule && (bUnloadAll || oModule.state === PRELOADED) ) {
				  delete mModules[sURN];
				}
			});

		};

		/**
		 * Converts a UI5 module name to a unified resource name.
		 *
		 * Used by View and Fragment APIs to convert a given module name into a unified resource name.
		 * When the <code>sSuffix</code> is not given, the suffix '.js' is added. This fits the most
		 * common use case of converting a module name to the Javascript resource that contains the
		 * module. Note that an empty <code>sSuffix</code> is not replaced by '.js'. This allows to
		 * convert UI5 module names to requireJS module names with a call to this method.
		 *
		 * @param {string} sModuleName Module name as a dot separated name
		 * @param {string} [sSuffix='.js'] Suffix to add to the final resource name
		 * @private
		 * @sap-restricted sap.ui.core
		 */
		jQuery.sap.getResourceName = function(sModuleName, sSuffix) {
			return ui5ToRJS(sModuleName) + (sSuffix == null ? ".js" : sSuffix);
		};

		/**
		 * Retrieves the resource with the given name, either from the preload cache or from
		 * the server. The expected data type of the resource can either be specified in the
		 * options (<code>dataType</code>) or it will be derived from the suffix of the <code>sResourceName</code>.
		 * The only supported data types so far are xml, html, json and text. If the resource name extension
		 * doesn't match any of these extensions, the data type must be specified in the options.
		 *
		 * If the resource is found in the preload cache, it will be converted from text format
		 * to the requested <code>dataType</code> using a converter from <code>jQuery.ajaxSettings.converters</code>.
		 *
		 * If it is not found, the resource name will be converted to a resource URL (using {@link #getResourcePath})
		 * and the resulting URL will be requested from the server with a synchronous jQuery.ajax call.
		 *
		 * If the resource was found in the local preload cache and any necessary conversion succeeded
		 * or when the resource was retrieved from the backend successfully, the content of the resource will
		 * be returned. In any other case, an exception will be thrown, or if option failOnError is set to true,
		 * <code>null</code> will be returned.
		 *
		 * Future implementations of this API might add more options. Generic implementations that accept an
		 * <code>mOptions</code> object and propagate it to this function should limit the options to the currently
		 * defined set of options or they might fail for unknown options.
		 *
		 * For asynchronous calls the return value of this method is an ECMA Script 6 Promise object which callbacks are triggered
		 * when the resource is ready:
		 * If <code>failOnError</code> is <code>false</code> the catch callback of the promise is not called. The argument given to the fullfilled
		 * callback is null in error case.
		 * If <code>failOnError</code> is <code>true</code> the catch callback will be triggered. The argument is an Error object in this case.
		 *
		 * @param {string} [sResourceName] resourceName in unified resource name syntax
		 * @param {object} [mOptions] options
		 * @param {object} [mOptions.dataType] one of "xml", "html", "json" or "text". If not specified it will be derived from the resource name (extension)
		 * @param {string} [mOptions.name] unified resource name of the resource to load (alternative syntax)
		 * @param {string} [mOptions.url] url of a resource to load (alternative syntax, name will only be a guess)
		 * @param {string} [mOptions.headers] Http headers for an eventual XHR request
		 * @param {string} [mOptions.failOnError=true] whether to propagate load errors or not
		 * @param {string} [mOptions.async=false] whether the loading should be performed asynchronously.
		 * @return {string|Document|object|Promise} content of the resource. A string for text or html, an Object for JSON, a Document for XML. For asynchronous calls an ECMA Script 6 Promise object will be returned.
		 * @throws Error if loading the resource failed
		 * @private
		 * @experimental API is not yet fully mature and may change in future.
		 * @since 1.15.1
		 */
		jQuery.sap.loadResource = function(sResourceName, mOptions) {

			var sType,
				oData,
				sUrl,
				oError,
				oDeferred;

			if ( typeof sResourceName === "string" ) {
				mOptions = mOptions || {};
			} else {
				mOptions = sResourceName || {};
				sResourceName = mOptions.name;
				if ( !sResourceName && mOptions.url) {
					sResourceName = guessResourceName(mOptions.url);
				}
			}
			// defaulting
			mOptions = jQuery.extend({ failOnError: true, async: false }, mOptions);

			sType = mOptions.dataType;
			if ( sType == null && sResourceName ) {
				sType = (sType = rTypes.exec(sResourceName)) && sType[1];
			}

			jQuery.sap.assert(/^(xml|html|json|text)$/.test(sType), "type must be one of xml, html, json or text");

			oDeferred = mOptions.async ? new jQuery.Deferred() : null;

			function handleData(d, e) {
				if ( d == null && mOptions.failOnError ) {
					oError = e || new Error("no data returned for " + sResourceName);
					if (mOptions.async) {
						oDeferred.reject(oError);
						jQuery.sap.log.error(oError);
					}
					return null;
				}

				if (mOptions.async) {
					oDeferred.resolve(d);
				}

				return d;
			}

			function convertData(d) {
				var vConverter = jQuery.ajaxSettings.converters["text " + sType];
				if ( typeof vConverter === "function" ) {
					d = vConverter(d);
				}
				return handleData(d);
			}

			if ( sResourceName && mModules[sResourceName] ) {
				oData = mModules[sResourceName].data;
				mModules[sResourceName].state = LOADED;
			}

			if ( oData != null ) {

				if (mOptions.async) {
					//Use timeout to simulate async behavior for this sync case for easier usage
					setTimeout(function(){
						convertData(oData);
					}, 0);
				} else {
					oData = convertData(oData);
				}

			} else {

				if ( !mOptions.async && syncCallBehavior ) {
					if ( syncCallBehavior >= 1 ) { // temp. raise a warning only
						log.error("[nosync] loading resource '" + (sResourceName || mOptions.url) + "' with sync XHR");
					} else {
						throw new Error("[nosync] loading resource '" + (sResourceName || mOptions.url) + "' with sync XHR");
					}
				}

				jQuery.ajax({
					url : sUrl = mOptions.url || getResourcePath(sResourceName),
					async : mOptions.async,
					dataType : sType,
					headers: mOptions.headers,
					success : function(data, textStatus, xhr) {
						oData = handleData(data);
					},
					error : function(xhr, textStatus, error) {
						oError = new Error("resource " + sResourceName + " could not be loaded from " + sUrl + ". Check for 'file not found' or parse errors. Reason: " + error);
						oError.status = textStatus;
						oError.error = error;
						oError.statusCode = xhr.status;
						oData = handleData(null, oError);
					}
				});

			}

			if ( mOptions.async ) {
				return Promise.resolve(oDeferred);
			}

			if ( oError != null && mOptions.failOnError ) {
				throw oError;
			}

			return oData;
		};

		/*
		 * register a global event handler to detect script execution errors.
		 * Only works for browsers that support document.currentScript.
		 * /
		window.addEventListener("error", function(e) {
			if ( document.currentScript && document.currentScript.dataset.sapUiModule ) {
				var error = {
					message: e.message,
					filename: e.filename,
					lineno: e.lineno,
					colno: e.colno
				};
				document.currentScript.dataset.sapUiModuleError = JSON.stringify(error);
			}
		});
		*/

		/**
		 * Loads the given Javascript resource (URN) asynchronously via as script tag.
		 * Returns a promise that will be resolved when the load event is fired or reject
		 * when the error event is fired.
		 *
		 * Note: execution errors of the script are not reported as 'error'.
		 *
		 * This method is not a full implementation of require. It is intended only for
		 * loading "preload" files that do not define an own module / module value.
		 *
		 * Functionality might be removed/renamed in future, so no code outside the
		 * sap.ui.core library must use it.
		 *
		 * @experimental
		 * @private
		 * @sap-restricted sap.ui.core,sap.ushell
		 */
		jQuery.sap._loadJSResourceAsync = function(sResource, bIgnoreErrors) {

			var oModule = Module.get(sResource);

			if ( !oModule.loaded ) {

				oModule.loaded = new Promise(function(resolve,reject) {

					function onload(e) {
						jQuery.sap.log.info("Javascript resource loaded: " + sResource);
						// TODO either find a cross-browser solution to detect and assign execution errors or document behavior
						//var error = e.target.dataset.sapUiModuleError;
						//if ( error ) {
						//	oModule.state = FAILED;
						//	oModule.error = JSON.parse(error);
						//	jQuery.sap.log.error("failed to load Javascript resource: " + sResource + ":" + error);
						//	reject(oModule.error);
						//}
						oScript.removeEventListener('load', onload);
						oScript.removeEventListener('error', onerror);
						oModule.state = READY;
						// TODO oModule.data = ?
						resolve();
					}

					function onerror(e) {
						jQuery.sap.log.error("failed to load Javascript resource: " + sResource);
						oScript.removeEventListener('load', onload);
						oScript.removeEventListener('error', onerror);
						oModule.state = FAILED;
						// TODO oModule.error = xhr ? xhr.status + " - " + xhr.statusText : textStatus;
						reject();
					}

					var sUrl = oModule.url = getResourcePath(sResource);
					oModule.state = LOADING;

					var oScript = window.document.createElement('SCRIPT');
					oScript.src = sUrl;
					oScript.setAttribute("data-sap-ui-module", sResource); // IE9/10 don't support dataset :-(
					// oScript.setAttribute("data-sap-ui-module-error", '');
					oScript.addEventListener('load', onload);
					oScript.addEventListener('error', onerror);
					appendHead(oScript);
				});

			}

			if ( bIgnoreErrors ) {
				return oModule.loaded.catch(function() {
					return undefined;
				});
			}

			return oModule.loaded;
		};

		return function() {

			//remove final information in mUrlPrefixes
			var mFlatUrlPrefixes = {};
				jQuery.each(mUrlPrefixes, function(sKey,oUrlPrefix) {
				mFlatUrlPrefixes[sKey] = oUrlPrefix.url;
			});


			return { modules : mModules, prefixes : mFlatUrlPrefixes };
		};

	}());

	// --------------------- script and stylesheet handling --------------------------------------------------

	// appends a link object to the head
	function appendHead(oElement) {
		var head = window.document.getElementsByTagName("head")[0];
		if (head) {
			head.appendChild(oElement);
		}
	}

	function _includeScript(sUrl, mAttributes, fnLoadCallback, fnErrorCallback) {
		var oScript = window.document.createElement("script");
		oScript.src = sUrl;
		oScript.type = "text/javascript";
		if (typeof mAttributes === "object") {
			Object.keys(mAttributes).forEach(function(sKey) {
				if (mAttributes[sKey] != null) {
					oScript.setAttribute(sKey, mAttributes[sKey]);
				}
			});
		}

		if (fnLoadCallback) {
			jQuery(oScript).load(function() {
				fnLoadCallback();
				jQuery(oScript).off("load");
			});
		}

		if (fnErrorCallback) {
			jQuery(oScript).error(function() {
				fnErrorCallback();
				jQuery(oScript).off("error");
			});
		}

		// jQuery("head").append(oScript) doesn't work because they filter for the script
		// and execute them directly instead adding the SCRIPT tag to the head
		var oOld, sId = mAttributes && mAttributes.id;
		if ((sId && (oOld = jQuery.sap.domById(sId)) && oOld.tagName === "SCRIPT")) {
			jQuery(oOld).remove(); // replacing scripts will not trigger the load event
		}
		appendHead(oScript);
	}

	/**
	 * Includes the script (via &lt;script&gt;-tag) into the head for the
	 * specified <code>sUrl</code> and optional <code>sId</code>.
	 *
	 * @param {string|object}
	 *            vUrl the URL of the script to load or a configuration object
	 * @param {string}
	 *            vUrl.url the URL of the script to load
	 * @param {string}
	 *            [vUrl.id] id that should be used for the script tag
	 * @param {object}
	 *            [vUrl.attributes] map of attributes that should be used for the script tag
	 * @param {string|object}
	 *            [vId] id that should be used for the script tag or map of attributes
	 * @param {function}
	 *            [fnLoadCallback] callback function to get notified once the script has been loaded
	 * @param {function}
	 *            [fnErrorCallback] callback function to get notified once the script loading failed
	 * @return {void|Promise}
	 *            When using the configuration object a <code>Promise</code> will be returned. The
	 *            documentation for the <code>fnLoadCallback</code> applies to the <code>resolve</code>
	 *            handler of the <code>Promise</code> and the one for the <code>fnErrorCallback</code>
	 *            applies to the <code>reject</code> handler of the <code>Promise</code>.
	 *
	 * @public
	 * @static
	 * @SecSink {0|PATH} Parameter is used for future HTTP requests
	 */
	jQuery.sap.includeScript = function includeScript(vUrl, vId, fnLoadCallback, fnErrorCallback) {
		if (typeof vUrl === "string") {
			var mAttributes = typeof vId === "string" ? {id: vId} : vId;
			_includeScript(vUrl, mAttributes, fnLoadCallback, fnErrorCallback);
		} else {
			jQuery.sap.assert(typeof vUrl === 'object' && vUrl.url, "vUrl must be an object and requires a URL");
			if (vUrl.id) {
				vUrl.attributes = vUrl.attributes || {};
				vUrl.attributes.id = vUrl.id;
			}
			return new Promise(function(fnResolve, fnReject) {
				_includeScript(vUrl.url, vUrl.attributes, fnResolve, fnReject);
			});
		}
	};

	function _includeStyleSheet(sUrl, mAttributes, fnLoadCallback, fnErrorCallback) {

		var _createLink = function(sUrl, mAttributes, fnLoadCallback, fnErrorCallback){

			// create the new link element
			var oLink = document.createElement("link");
			oLink.type = "text/css";
			oLink.rel = "stylesheet";
			oLink.href = sUrl;
			if (typeof mAttributes === "object") {
				Object.keys(mAttributes).forEach(function(sKey) {
					if (mAttributes[sKey] != null) {
						oLink.setAttribute(sKey, mAttributes[sKey]);
					}
				});
			}

			var fnError = function() {
				jQuery(oLink).attr("data-sap-ui-ready", "false").off("error");
				if (fnErrorCallback) {
					fnErrorCallback();
				}
			};

			var fnLoad = function() {
				jQuery(oLink).attr("data-sap-ui-ready", "true").off("load");
				if (fnLoadCallback) {
					fnLoadCallback();
				}
			};

			// for IE we will check if the stylesheet contains any rule and then
			// either trigger the load callback or the error callback
			if ( Device.browser.msie ) {
				var fnLoadOrg = fnLoad;
				fnLoad = function(oEvent) {
					var aRules;
					try {
						// in cross-origin scenarios the IE can still access the rules of the stylesheet
						// if the stylesheet has been loaded properly
						aRules = oEvent.target && oEvent.target.sheet && oEvent.target.sheet.rules;
						// in cross-origin scenarios now the catch block will be executed because we
						// cannot access the rules of the stylesheet but for non cross-origin stylesheets
						// we will get an empty rules array and finally we cannot differ between
						// empty stylesheet or loading issue correctly => documented in JSDoc!
					} catch (ex) {
						// exception happens when the stylesheet could not be loaded from the server
						// we now ignore this and know that the stylesheet doesn't exists => trigger error
					}
					// no rules means error
					if (aRules && aRules.length > 0) {
						fnLoadOrg();
					} else {
						fnError();
					}
				};
			}

			jQuery(oLink).load(fnLoad);
			jQuery(oLink).error(fnError);
			return oLink;

		};

		// check for existence of the link
		var oLink = _createLink(sUrl, mAttributes, fnLoadCallback, fnErrorCallback);
		var oOld = jQuery.sap.domById(mAttributes && mAttributes.id);
		if (oOld && oOld.tagName === "LINK" && oOld.rel === "stylesheet") {
			// link exists, so we replace it - but only if a callback has to be attached or if the href will change. Otherwise don't touch it
			if (fnLoadCallback || fnErrorCallback || oOld.href !== URI(String(sUrl), URI().search("") /* returns current URL without search params */ ).toString()) {
				jQuery(oOld).replaceWith(oLink);
			}
		} else {
			oOld = jQuery('#sap-ui-core-customcss');
			if (oOld.length > 0) {
				oOld.first().before(oLink);
			} else {
				appendHead(oLink);
			}
		}

	}

	/**
	 * Includes the specified stylesheet via a &lt;link&gt;-tag in the head of the current document. If there is call to
	 * <code>includeStylesheet</code> providing the sId of an already included stylesheet, the existing element will be
	 * replaced.
	 *
	 * @param {string|object}
	 *          vUrl the URL of the stylesheet to load or a configuration object
	 * @param {string}
	 *            vUrl.url the URL of the stylesheet to load
	 * @param {string}
	 *            [vUrl.id] id that should be used for the link tag
	 * @param {object}
	 *            [vUrl.attributes] map of attributes that should be used for the script tag
	 * @param {string|object}
	 *          [vId] id that should be used for the link tag or map of attributes
	 * @param {function}
	 *          [fnLoadCallback] callback function to get notified once the stylesheet has been loaded
	 * @param {function}
	 *          [fnErrorCallback] callback function to get notified once the stylesheet loading failed.
	 *            In case of usage in IE the error callback will also be executed if an empty stylesheet
	 *            is loaded. This is the only option how to determine in IE if the load was successful
	 *            or not since the native onerror callback for link elements doesn't work in IE. The IE
	 *            always calls the onload callback of the link element.
	 *            Another issue of the IE9 is that in case of loading too many stylesheets the eventing
	 *            is not working and therefore the error or load callback will not be triggered anymore.
	 * @return {void|Promise}
	 *            When using the configuration object a <code>Promise</code> will be returned. The
	 *            documentation for the <code>fnLoadCallback</code> applies to the <code>resolve</code>
	 *            handler of the <code>Promise</code> and the one for the <code>fnErrorCallback</code>
	 *            applies to the <code>reject</code> handler of the <code>Promise</code>.
	 *
	 * @public
	 * @static
	 * @SecSink {0|PATH} Parameter is used for future HTTP requests
	 */
	jQuery.sap.includeStyleSheet = function includeStyleSheet(vUrl, vId, fnLoadCallback, fnErrorCallback) {
		if (typeof vUrl === "string") {
			var mAttributes = typeof vId === "string" ? {id: vId} : vId;
			_includeStyleSheet(vUrl, mAttributes, fnLoadCallback, fnErrorCallback);
		} else {
			jQuery.sap.assert(typeof vUrl === 'object' && vUrl.url, "vUrl must be an object and requires a URL");
			if (vUrl.id) {
				vUrl.attributes = vUrl.attributes || {};
				vUrl.attributes.id = vUrl.id;
			}
			return new Promise(function(fnResolve, fnReject) {
				_includeStyleSheet(vUrl.url, vUrl.attributes, fnResolve, fnReject);
			});
		}
	};

	// --------------------- support hooks ---------------------------------------------------------

	// TODO should be in core, but then the 'callback' could not be implemented
	if ( !(oCfgData.productive === true || oCfgData.productive === "true"  || oCfgData.productive === "x") ) {
		document.addEventListener('keydown', function(e) {
			try {
				if ( e.shiftKey && e.altKey && e.ctrlKey ) {
					if ( e.keyCode === 80 ) { // 'P'
						sap.ui.require(['sap/ui/debug/TechnicalInfo'], function(TechnicalInfo) {
							TechnicalInfo.open(function() {
								var oInfo = getModuleSystemInfo();
								return { modules : oInfo.modules, prefixes : oInfo.prefixes, config: oCfgData };
							});
						});
					} else if ( e.keyCode === 83 ) { // 'S'
						sap.ui.require(['sap/ui/core/support/Support'], function(Support) {
							var oSupport = Support.getStub();
							if (oSupport.getType() != Support.StubType.APPLICATION) {
								return;
							}
							oSupport.openSupportTool();
						});
					}
				}
			} catch (err) {
				// ignore any errors
			}
		});
	}

	// --------------------- feature detection, enriching jQuery.support  ----------------------------------------------------

	// this might go into its own file once there is more stuff added

	/**
	 * Holds information about the browser's capabilities and quirks.
	 * This object is provided and documented by jQuery.
	 * But it is extended by SAPUI5 with detection for features not covered by jQuery. This documentation ONLY covers the detection properties added by UI5.
	 * For the standard detection properties, please refer to the jQuery documentation.
	 *
	 * These properties added by UI5 are only available temporarily until jQuery adds feature detection on their own.
	 *
	 * @name jQuery.support
	 * @namespace
	 * @since 1.12
	 * @public
	 */

	if (!jQuery.support) {
		jQuery.support = {};
	}

	jQuery.extend(jQuery.support, {touch: Device.support.touch}); // this is also defined by jquery-mobile-custom.js, but this information is needed earlier

	var aPrefixes = ["Webkit", "ms", "Moz"];
	var oStyle = document.documentElement.style;

	var preserveOrTestCssPropWithPrefixes = function(detectionName, propName) {
		if (jQuery.support[detectionName] === undefined) {

			if (oStyle[propName] !== undefined) { // without vendor prefix
				jQuery.support[detectionName] = true;
				// If one of the flex layout properties is supported without the prefix, set the flexBoxPrefixed to false
				if (propName === "boxFlex" || propName === "flexOrder" || propName === "flexGrow") {
					// Exception for Chrome up to version 28
					// because some versions implemented the non-prefixed properties without the functionality
					if (!Device.browser.chrome || Device.browser.version > 28) {
						jQuery.support.flexBoxPrefixed = false;
					}
				}
				return;

			} else { // try vendor prefixes
				propName = propName.charAt(0).toUpperCase() + propName.slice(1);
				for (var i in aPrefixes) {
					if (oStyle[aPrefixes[i] + propName] !== undefined) {
						jQuery.support[detectionName] = true;
						return;
					}
				}
			}
			jQuery.support[detectionName] = false;
		}
	};

	/**
	 * Whether the current browser supports (2D) CSS transforms
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.cssTransforms
	 */
	preserveOrTestCssPropWithPrefixes("cssTransforms", "transform");

	/**
	 * Whether the current browser supports 3D CSS transforms
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.cssTransforms3d
	 */
	preserveOrTestCssPropWithPrefixes("cssTransforms3d", "perspective");

	/**
	 * Whether the current browser supports CSS transitions
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.cssTransitions
	 */
	preserveOrTestCssPropWithPrefixes("cssTransitions", "transition");

	/**
	 * Whether the current browser supports (named) CSS animations
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.cssAnimations
	 */
	preserveOrTestCssPropWithPrefixes("cssAnimations", "animationName");

	/**
	 * Whether the current browser supports CSS gradients. Note that ANY support for CSS gradients leads to "true" here, no matter what the syntax is.
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.cssGradients
	 */
	if (jQuery.support.cssGradients === undefined) {
		var oElem = document.createElement('div'),
		oStyle = oElem.style;
		try {
			oStyle.backgroundImage = "linear-gradient(left top, red, white)";
			oStyle.backgroundImage = "-moz-linear-gradient(left top, red, white)";
			oStyle.backgroundImage = "-webkit-linear-gradient(left top, red, white)";
			oStyle.backgroundImage = "-ms-linear-gradient(left top, red, white)";
			oStyle.backgroundImage = "-webkit-gradient(linear, left top, right bottom, from(red), to(white))";
		} catch (e) {/* no support...*/}
		jQuery.support.cssGradients = (oStyle.backgroundImage && oStyle.backgroundImage.indexOf("gradient") > -1);

		oElem = null; // free for garbage collection
	}

	/**
	 * Whether the current browser supports only prefixed flexible layout properties
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.flexBoxPrefixed
	 */
	jQuery.support.flexBoxPrefixed = true;	// Default to prefixed properties

	/**
	 * Whether the current browser supports the OLD CSS3 Flexible Box Layout directly or via vendor prefixes
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.flexBoxLayout
	 */
	preserveOrTestCssPropWithPrefixes("flexBoxLayout", "boxFlex");

	/**
	 * Whether the current browser supports the NEW CSS3 Flexible Box Layout directly or via vendor prefixes
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.newFlexBoxLayout
	 */
	preserveOrTestCssPropWithPrefixes("newFlexBoxLayout", "flexGrow");	// Use a new property that IE10 doesn't support

	/**
	 * Whether the current browser supports the IE10 CSS3 Flexible Box Layout directly or via vendor prefixes
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.ie10FlexBoxLayout
	 * @since 1.12.0
	 */
	// Just using one of the IE10 properties that's not in the new FlexBox spec
	if (!jQuery.support.newFlexBoxLayout && oStyle.msFlexOrder !== undefined) {
		jQuery.support.ie10FlexBoxLayout = true;
	} else {
		jQuery.support.ie10FlexBoxLayout = false;
	}

	/**
	 * Whether the current browser supports any kind of Flexible Box Layout directly or via vendor prefixes
	 * @type {boolean}
	 * @public
	 * @name jQuery.support.hasFlexBoxSupport
	 */
	if (jQuery.support.flexBoxLayout || jQuery.support.newFlexBoxLayout || jQuery.support.ie10FlexBoxLayout) {
		jQuery.support.hasFlexBoxSupport = true;
	} else {
		jQuery.support.hasFlexBoxSupport = false;
	}

	// --------------------- frame protection -------------------------------------------------------

	/**
	 * FrameOptions class
	 */
	var FrameOptions = function(mSettings) {
		/* mSettings: mode, callback, whitelist, whitelistService, timeout, blockEvents, showBlockLayer, allowSameOrigin */
		this.mSettings = mSettings || {};
		this.sMode = this.mSettings.mode || FrameOptions.Mode.ALLOW;
		this.fnCallback = this.mSettings.callback;
		this.iTimeout = this.mSettings.timeout || 10000;
		this.bBlockEvents = this.mSettings.blockEvents !== false;
		this.bShowBlockLayer = this.mSettings.showBlockLayer !== false;
		this.bAllowSameOrigin = this.mSettings.allowSameOrigin !== false;
		this.sParentOrigin = '';
		this.bUnlocked = false;
		this.bRunnable = false;
		this.bParentUnlocked = false;
		this.bParentResponded = false;
		this.sStatus = "pending";
		this.aFPChilds = [];

		var that = this;

		this.iTimer = setTimeout(function() {
			that._callback(false);
		}, this.iTimeout);

		var fnHandlePostMessage = function() {
			that._handlePostMessage.apply(that, arguments);
		};

		FrameOptions.__window.addEventListener('message', fnHandlePostMessage);

		if (FrameOptions.__parent === FrameOptions.__self || FrameOptions.__parent == null || this.sMode === FrameOptions.Mode.ALLOW) {
			// unframed page or "allow all" mode
			this._applyState(true, true);
		} else {
			// framed page

			this._lock();

			// "deny" mode blocks embedding page from all origins
			if (this.sMode === FrameOptions.Mode.DENY) {
				this._callback(false);
				return;
			}

			if (this.bAllowSameOrigin) {

				try {
					var oParentWindow = FrameOptions.__parent;
					var bOk = false;
					var bTrue = true;
					do {
						var test = oParentWindow.document.domain;
						if (oParentWindow == FrameOptions.__top) {
							if (test != undefined) {
								bOk = true;
							}
							break;
						}
						oParentWindow = oParentWindow.parent;
					} while (bTrue);
					if (bOk) {
						this._applyState(true, true);
					}
				} catch (e) {
					// access to the top window is not possible
					this._sendRequireMessage();
				}

			} else {
				// same origin not allowed
				this._sendRequireMessage();
			}

		}

	};

	FrameOptions.Mode = {
		// only allow with same origin parent
		TRUSTED: 'trusted',

		// allow all kind of embedding (default)
		ALLOW: 'allow',

		// deny all kinds of embedding
		DENY: 'deny'
	};

	// Allow globals to be mocked in unit test
	FrameOptions.__window = window;
	FrameOptions.__parent = parent;
	FrameOptions.__self = self;
	FrameOptions.__top = top;

	// List of events to block while framing is unconfirmed
	FrameOptions._events = [
		"mousedown", "mouseup", "click", "dblclick", "mouseover", "mouseout",
		"touchstart", "touchend", "touchmove", "touchcancel",
		"keydown", "keypress", "keyup"
	];

	// check if string matches pattern
	FrameOptions.prototype.match = function(sProbe, sPattern) {
		if (!(/\*/i.test(sPattern))) {
			return sProbe == sPattern;
		} else {
			sPattern = sPattern.replace(/\//gi, "\\/"); // replace /   with \/
			sPattern = sPattern.replace(/\./gi, "\\."); // replace .   with \.
			sPattern = sPattern.replace(/\*/gi, ".*");  // replace *   with .*
			sPattern = sPattern.replace(/:\.\*$/gi, ":\\d*"); // replace :.* with :\d* (only at the end)

			if (sPattern.substr(sPattern.length - 1, 1) !== '$') {
				sPattern = sPattern + '$'; // if not already there add $ at the end
			}
			if (sPattern.substr(0, 1) !== '^') {
				sPattern = '^' + sPattern; // if not already there add ^ at the beginning
			}

			// sPattern looks like: ^.*:\/\/.*\.company\.corp:\d*$ or ^.*\.company\.corp$
			var r = new RegExp(sPattern, 'i');
			return r.test(sProbe);
		}
	};

	FrameOptions._lockHandler = function(oEvent) {
		oEvent.stopPropagation();
		oEvent.preventDefault();
	};

	FrameOptions.prototype._createBlockLayer = function() {
		if (document.readyState == "complete") {
			var lockDiv = document.createElement("div");
			lockDiv.style.position = "absolute";
			lockDiv.style.top = "-1000px";
			lockDiv.style.bottom = "-1000px";
			lockDiv.style.left = "-1000px";
			lockDiv.style.right = "-1000px";
			lockDiv.style.opacity = "0";
			lockDiv.style.backgroundColor = "white";
			lockDiv.style.zIndex = 2147483647; // Max value of signed integer (32bit)
			document.body.appendChild(lockDiv);
			this._lockDiv = lockDiv;
		}
	};

	FrameOptions.prototype._setCursor = function() {
		if (this._lockDiv) {
			this._lockDiv.style.cursor = this.sStatus == "denied" ? "not-allowed" : "wait";
		}
	};

	FrameOptions.prototype._lock = function() {
		var that = this;
		if (this.bBlockEvents) {
			for (var i = 0; i < FrameOptions._events.length; i++) {
				document.addEventListener(FrameOptions._events[i], FrameOptions._lockHandler, true);
			}
		}
		if (this.bShowBlockLayer) {
			this._blockLayer = function() {
				that._createBlockLayer();
				that._setCursor();
			};
			if (document.readyState == "complete") {
				this._blockLayer();
			} else {
				document.addEventListener("readystatechange", this._blockLayer);
			}
		}
	};

	FrameOptions.prototype._unlock = function() {
		if (this.bBlockEvents) {
			for (var i = 0; i < FrameOptions._events.length; i++) {
				document.removeEventListener(FrameOptions._events[i], FrameOptions._lockHandler, true);
			}
		}
		if (this.bShowBlockLayer) {
			document.removeEventListener("readystatechange", this._blockLayer);
			if (this._lockDiv) {
				document.body.removeChild(this._lockDiv);
				delete this._lockDiv;
			}
		}
	};

	FrameOptions.prototype._callback = function(bSuccess) {
		this.sStatus = bSuccess ? "allowed" : "denied";
		this._setCursor();
		clearTimeout(this.iTimer);
		if (typeof this.fnCallback === 'function') {
			this.fnCallback.call(null, bSuccess);
		}
	};

	FrameOptions.prototype._applyState = function(bIsRunnable, bIsParentUnlocked) {
		if (this.bUnlocked) {
			return;
		}
		if (bIsRunnable) {
			this.bRunnable = true;
		}
		if (bIsParentUnlocked) {
			this.bParentUnlocked = true;
		}
		if (!this.bRunnable || !this.bParentUnlocked) {
			return;
		}
		this._unlock();
		this._callback(true);
		this._notifyChildFrames();
		this.bUnlocked = true;
	};

	FrameOptions.prototype._applyTrusted = function(bTrusted) {
		if (bTrusted) {
			this._applyState(true, false);
		} else {
			this._callback(false);
		}
	};

	FrameOptions.prototype._check = function(bParentResponsePending) {
		if (this.bRunnable) {
			return;
		}
		var bTrusted = false;
		if (this.bAllowSameOrigin && this.sParentOrigin && FrameOptions.__window.document.URL.indexOf(this.sParentOrigin) == 0) {
			bTrusted = true;
		} else if (this.mSettings.whitelist && this.mSettings.whitelist.length != 0) {
			var sHostName = this.sParentOrigin.split('//')[1];
			sHostName = sHostName.split(':')[0];
			for (var i = 0; i < this.mSettings.whitelist.length; i++) {
				var match = sHostName.indexOf(this.mSettings.whitelist[i]);
				if (match != -1 && sHostName.substring(match) == this.mSettings.whitelist[i]) {
					bTrusted = true;
					break;
				}
			}
		}
		if (bTrusted) {
			this._applyTrusted(bTrusted);
		} else if (this.mSettings.whitelistService) {
			var that = this;
			var xmlhttp = new XMLHttpRequest();
			var url = this.mSettings.whitelistService + '?parentOrigin=' + encodeURIComponent(this.sParentOrigin);
			xmlhttp.onreadystatechange = function() {
				if (xmlhttp.readyState == 4) {
					that._handleXmlHttpResponse(xmlhttp, bParentResponsePending);
				}
			};
			xmlhttp.open('GET', url, true);
			xmlhttp.setRequestHeader('Accept', 'application/json');
			xmlhttp.send();
		} else {
			this._callback(false);
		}
	};

	FrameOptions.prototype._handleXmlHttpResponse = function(xmlhttp, bParentResponsePending) {
		if (xmlhttp.status === 200) {
			var bTrusted = false;
			var sResponseText = xmlhttp.responseText;
			var oRuleSet = JSON.parse(sResponseText);
			if (oRuleSet.active == false) {
				this._applyState(true, true);
			} else if (bParentResponsePending) {
				return;
			} else {
				if (this.match(this.sParentOrigin, oRuleSet.origin)) {
					bTrusted = oRuleSet.framing;
				}
				this._applyTrusted(bTrusted);
			}
		} else {
			jQuery.sap.log.warning("The configured whitelist service is not available: " + xmlhttp.status);
			this._callback(false);
		}
	};

	FrameOptions.prototype._notifyChildFrames = function() {
		for (var i = 0; i < this.aFPChilds.length; i++) {
			this.aFPChilds[i].postMessage('SAPFrameProtection*parent-unlocked','*');
		}
	};

	FrameOptions.prototype._sendRequireMessage = function() {
		FrameOptions.__parent.postMessage('SAPFrameProtection*require-origin', '*');
		// If not postmessage response was received, send request to whitelist service
		// anyway, to check whether frame protection is enabled
		if (this.mSettings.whitelistService) {
			setTimeout(function() {
				if (!this.bParentResponded) {
					this._check(true);
				}
			}.bind(this), 10);
		}
	};

	FrameOptions.prototype._handlePostMessage = function(oEvent) {
		var oSource = oEvent.source,
			sData = oEvent.data;

		// For compatibility with previous version empty message from parent means parent-unlocked
		// if (oSource === FrameOptions.__parent && sData == "") {
		//	sData = "SAPFrameProtection*parent-unlocked";
		// }

		if (oSource === FrameOptions.__self || oSource == null ||
			typeof sData !== "string" || sData.indexOf("SAPFrameProtection*") === -1) {
			return;
		}
		if (oSource === FrameOptions.__parent) {
			this.bParentResponded = true;
			if (!this.sParentOrigin) {
				this.sParentOrigin = oEvent.origin;
				this._check();
			}
			if (sData == "SAPFrameProtection*parent-unlocked") {
				this._applyState(false, true);
			}
		} else if (oSource.parent === FrameOptions.__self && sData == "SAPFrameProtection*require-origin" && this.bUnlocked) {
			oSource.postMessage("SAPFrameProtection*parent-unlocked", "*");
		} else {
			oSource.postMessage("SAPFrameProtection*parent-origin", "*");
			this.aFPChilds.push(oSource);
		}
	};

	jQuery.sap.FrameOptions = FrameOptions;

}(jQuery, sap.ui.Device, window));

/**
 * Executes an 'eval' for its arguments in the global context (without closure variables).
 *
 * This is a synchronous replacement for <code>jQuery.globalEval</code> which in some
 * browsers (e.g. FireFox) behaves asynchronously.
 *
 * @type void
 * @public
 * @static
 * @SecSink {0|XSS} Parameter is evaluated
 */
jQuery.sap.globalEval = function() {
	"use strict";

	/*eslint-disable no-eval */
	eval(arguments[0]);
	/*eslint-enable no-eval */
};
jQuery.sap.declare('sap-ui-core-nojQuery-dbg');
jQuery.sap.declare('sap.ui.Device', false);
jQuery.sap.declare('sap.ui.thirdparty.URI', false);
jQuery.sap.declare('sap.ui.thirdparty.es6-promise', false);
jQuery.sap.declare('jquery.sap.global', false);
jQuery.sap.require("sap.ui.core.Core");
// as this module contains the Core, we ensure that the Core has been booted
sap.ui.getCore().boot && sap.ui.getCore().boot();
//# sourceMappingURL=sap-ui-core-nojQuery-dbg.js.map