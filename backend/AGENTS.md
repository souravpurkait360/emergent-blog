## Do
- Always write APIViews
- Always write shared services and common helper methods in apps/core folder for reusability
- Always follow mentioned apps/ folder project structure for making new files or features
- Always write efficient bulk database operations whenever possible
- Always write unit and integration test cases after implementing a new feature
- Always run test cases on the files which you recently changed to make sure you do not break any existing functionality
- Always write better performant and highly optimized code based on the mentioned system specification
- Always write code that is thread safe
- Always use singleton pattern whenever possible
- Always throw exceptions from all layers and capture them explicitly in the api layer
- Always write import statements at the top of the file unless it throws circular dependency error
- Always create separate files for separate api views. 1 file should contain only 1 APIVIew class
- Always use descriptive variable names that reflect what the value represents (e.g. `subscription`, `transaction`, `item`)
- Always write optimized ORM queries in the repository layer and never in api or service layer
- Always make sure the number of lines of each file is less than 200. Break it into smaller modules if it is going beyond

## Don't
- Do not use single-letter or abbreviated variable names (e.g. `es`, `et`, `tv`, `ae`, `ie`) as standalone identifiers
- Do not use Model viewsets
- Do not hardcoded static values and use Enums for better maintainability
- Do not explicitly commit or rollback inside api or services layer as we are already doing that in the session manager
- Do not write N+1 queries
- Do not write inefficient database queries
- Do not assume microservices have certain API configuration unless explicitly mentioned
- Do not write try catch block in service layer unless necessary