# Do
- Always use tailwind css
- Always use tokenized colour/font/breakpoint variables in global level instead of component level
- Always keep the tailwind.config.js updated with latest token values in global level
- Always store fontsizes, colour codes, screensizes and all other tokens saved in tailwind configuration file
- Always make sure the pages and components are responsive to mobile, tablet, desktop and large monitors
- Always keep common components to components/common folder
- Always cache API responses and invalidate properly
- Always use Singleton design pattern
- Always show skeleton loaders/sheamers for loading animations
- Always remove unused variables
- Always modularize components of similar type in folders
- Always use zustand for local state management
- Always keep the sensitive values encrypted in most secure storages
- Always use common utilities for same type of functions
- Always use DRY principle
- Always keep the Parent components modular by breaking it down to multiple reusable components.

# Don't
- Do not use single-letter or abbreviated variable names (e.g. `s`, `t`, `v`, `e`, `i` as standalone identifiers in callbacks or map/filter/reduce). Always use descriptive names that reflect what the value represents (e.g. `status`, `transaction`, `item`).
- Do not hard coded colours anywhere in the app
- Do not use raw css anywhere
- Do not use Redux
- Do not store sensitive information in local storage or session storage or in plain text
- Do not write more than one functional component in a file
- Do not write more than 300 lines in a single component. 

## Data Flow

Parent page components own all API logic: queries, mutations, and handlers. They pass data and callbacks down to children via props. Children are presentational — they do not fetch their own data.