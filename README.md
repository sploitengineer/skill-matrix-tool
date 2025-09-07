# Tutorial: skill-matrix-tool

This tool is a **web application** that helps developers visualize their *programming language skills*. You enter a GitHub username, and it fetches data from their public repositories to analyze language usage and create an interactive "skill matrix" – a *radar chart* that visually represents your proficiency. It also offers a **REST API** for programmatic access to skill data and speeds things up by *caching* previously fetched information.


## Visual Overview

```mermaid
flowchart TD
    A0["Web Application Core
"]
    A1["GitHub Data Fetching & Processing
"]
    A2["Skill Matrix Graph Generation
"]
    A3["Database & Caching Service
"]
    A4["Data Normalization Utilities
"]
    A0 -- "Requests Data" --> A1
    A1 -- "Returns Processed Data" --> A0
    A0 -- "Requests Graph Generation" --> A2
    A2 -- "Generates Graph Files" --> A0
    A0 -- "Manages Data Storage" --> A3
    A3 -- "Provides Stored Data" --> A0
    A0 -- "Applies Normalization" --> A4
    A4 -- "Returns Normalized Scores" --> A0
```
