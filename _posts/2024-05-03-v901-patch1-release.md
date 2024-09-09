---
layout: post
title: WF TDM Version 9.0.1 - Official Release - Patch 1
categories: WF-TDM
author: Chris Day
---

A patch to the Wasatch Front Travel Demand Model (WF TDM) version 9.0.1 has been released. To access the new model, please visit the [WF TDM Official Releases Repository](https://github.com/WFRCAnalytics/WF-TDM-Official-Releases/releases/tag/v9.0.1-official). If do not have access to the repository please request access by emailing Suzie Swim at sswim@wfrc.org or Tim Hereth at thereth@mountainland.org.

The patch includes the following adjustments:

 1. An update related to SEGID and the SEGID exception fields was accidently left out of the official release published on 4/23/2024 causing the model to crash. The scripts were updated and added back into the model.
 2. A few minor edits were made to the highway network to correct the direction of a oneway frontage road link and to add a few nodes/links to make the network more consistent with v9.0.2 which is expected to be released in early June. The transit line files were edited to reflect the updated highway network added nodes/links.
