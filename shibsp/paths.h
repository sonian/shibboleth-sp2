/**
 * Licensed to the University Corporation for Advanced Internet
 * Development, Inc. (UCAID) under one or more contributor license
 * agreements. See the NOTICE file distributed with this work for
 * additional information regarding copyright ownership.
 *
 * UCAID licenses this file to you under the Apache License,
 * Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the
 * License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

/**
 * @file shibsp/paths.h
 * 
 * Default configuration paths.
 */

#ifndef __shibsp_paths_h__
#define __shibsp_paths_h__

/** Default schema catalogs. */
#define SHIBSP_SCHEMAS  "/home/scantor/opt/shibboleth-sp/share/xml/xmltooling/catalog.xml:/home/scantor/opt/shibboleth-sp/share/xml/opensaml/saml20-catalog.xml:/home/scantor/opt/shibboleth-sp/share/xml/opensaml/saml11-catalog.xml:/home/scantor/opt/shibboleth-sp/share/xml/shibboleth/catalog.xml"

/** Default prefix for installation (used to resolve relative paths). */
#define SHIBSP_PREFIX   "/home/scantor/opt/shibboleth-sp"

/** Library directory for installation (used to resolve relative paths). */
#define SHIBSP_LIBDIR   "/home/scantor/opt/shibboleth-sp/lib"

/** Log directory for installation (used to resolve relative paths). */
#define SHIBSP_LOGDIR   "/home/scantor/opt/shibboleth-sp/var/log"

/** Configuration directory for installation (used to resolve relative paths). */
#define SHIBSP_CFGDIR   "/home/scantor/opt/shibboleth-sp/etc"

/** Runtime state directory for installation (used to resolve relative paths). */
#define SHIBSP_RUNDIR   "/home/scantor/opt/shibboleth-sp/var/run"

/** Cache directory for installation (used to resolve relative paths). */
#define SHIBSP_CACHEDIR "/home/scantor/opt/shibboleth-sp/var/cache"

/** XML directory for installation (used to resolve relative paths). */
#define SHIBSP_XMLDIR   "/home/scantor/opt/shibboleth-sp/share/xml"

#endif /* __shibsp_paths_h__ */
