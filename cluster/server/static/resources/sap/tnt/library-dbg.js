/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

/**
 * Initialization Code and shared classes of library sap.tnt.
 */
sap.ui.define(['jquery.sap.global',
	'sap/ui/core/library', 'sap/m/library'], // library dependency
	function(jQuery) {

	'use strict';

	/**
	 * SAPUI5 library with controls specialized for administrative applications.
	 *
	 * @namespace
	 * @name sap.tnt
	 * @author SAP SE
	 * @version 1.46.7
	 * @public
	 */

	// delegate further initialization of this library to the Core
	sap.ui.getCore().initLibrary({
		name : 'sap.tnt',
		version: '1.46.7',
		dependencies : ['sap.ui.core','sap.m'],
		types: [],
		interfaces: [],
		controls: [
			'sap.tnt.NavigationList',
			'sap.tnt.ToolHeaderUtilitySeparator',
			'sap.tnt.ToolHeader',
			'sap.tnt.SideNavigation',
			'sap.tnt.ToolPage'
		],
		elements: [
			"sap.tnt.NavigationListItem"
		]
	});

	return sap.tnt;

});
