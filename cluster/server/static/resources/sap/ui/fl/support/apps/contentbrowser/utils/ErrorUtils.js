/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define("sap/ui/fl/support/apps/contentbrowser/utils/ErrorUtils",["sap/m/MessagePopoverItem","sap/m/MessagePopover"],function(M,a){"use strict";var E={};E._masterComponent=undefined;E._messagesModel=undefined;E._emptyModel=new sap.ui.model.json.JSONModel([]);E._messageTemplate=new M({type:"{messages>type}",title:"{messages>title}",description:"{messages>description}"});E._messagePopover=new a({items:{path:"messages>/",template:E._messageTemplate}});E.setMessagesModel=function(c,m){E._masterComponent=c;E._messagesModel=m;E._messagePopover.setModel(E._messagesModel,"messages");};E.handleMessagePopoverPress=function(s){E._messagePopover.openBy(s);};E.displayError=function(t,T,d){if(E._messagesModel){var m=E._messagesModel.getData();m.push({"type":t||"Information","title":T||"","description":d||""});E._messagesModel.setData(m);E._masterComponent.setModel(E._emptyModel,"messages");E._masterComponent.setModel(E._messagesModel,"messages");}};return E;});
