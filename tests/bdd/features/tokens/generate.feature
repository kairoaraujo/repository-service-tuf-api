Feature: Generate HTTP token for Repository Service for TUF (RSTUF)
    As an admin,
    Admin has deployed and bootstrapped RSTUF


    Scenario Outline: Admin uses HTTP API to generate a token
        Given the admin has the admin password
        And the admin gets an 'access_token' by logging in to '/api/v1/token' with a 'write:token' scope
        And the admin adds Authorization Bearer 'access_token' in the 'headers'
        And the admin adds JSON payload with scopes: <scopes> and expires: <expires>
        When the admin sends a POST request to '/api/v1/token/new'
        Then the admin should get status code '200'
        And the admin should get 'access_token' with a new token

        Examples:
            | scopes                                           | expires |
            | ['write:targets']                                | 1       |
            | ['write:targets', 'read:settings']               | 240     |
            | ['read:bootstrap']                               | 1       |
            | ['read:bootstrap','write:targets']               | 24      |
            | ['read:settings']                                | 3       |
            | ['read:token']                                   | 5       |
            | ['write:targets', 'read:settings', 'read:tasks'] | 380     |


   Scenario Outline: Admin cannot generate Token using HTTP API with an invalid expires
        Given the admin has the admin password
        And the admin gets an 'access_token' by logging in to '/api/v1/token' with a 'write:token' scope
        And the admin adds Authorization Bearer 'access_token' in the 'headers'
        And the admin adds JSON payload with scopes: <scopes> and expires: <expires>
        When the admin sends a POST request to '/api/v1/token/new' with invalid 'expires' in 'payload'
        Then the admin should get status code '422'

        Examples:
            | scopes                             | expires |
            | ['read:bootstrap','write:targets'] | 0       |
            | ['read:bootstrap','write:targets'] | -5      |
            | ['read:bootstrap']                 | None    |


   Scenario Outline: Admin cannot generate Token using HTTP API for certain scopes
        Given the admin has the admin password
        And the admin gets an 'access_token' by logging in to '/api/v1/token' with a 'write:token' scope
        And the admin adds Authorization Bearer 'access_token' in the 'headers'
        And the admin adds JSON payload with scopes: <scopes> and expires: <expires>
        When the admin sends a POST request to '/api/v1/token/new' with not allowed 'scopes' in 'payload'
        Then the admin should get status code '422'

        Examples:
            | scopes                               | expires |
            | ['write:token']                      | 24      |
            | ['read:bootstrap','write:token']     | 24      |
            | ['write:bootstrap']                  | 24      |
            | ['write:bootstrap', 'read:settings'] | 24      |
            | []                                   | 24      |
            | ['']                                 | 24      |

   Scenario Outline: Admin is Unauthorized to generate using HTTP API with an invalid token
        Given the admin adds Authorization Bearer <token> in the 'headers'
        And the admin adds JSON payload with scopes: <scopes> and expires: <expires>
        When the admin sends a POST request to '/api/v1/token/new' with invalid 'access_token' in the headers
        Then the admin should get status code '401'
        And the admin should get 'Failed to validate token' in the body

        Examples:
            | token       | scopes             | expires |
            | invalid     | ['write:targets']  | 1       |
            | eyJhbiJIUzI | ['read:bootstrap'] | 1       |
            | ''          | ['read:bootstrap'] | 1       |
