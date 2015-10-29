#Globus Auth Client Example

Simple [Flask](http://flask.pocoo.org/) application to demonstrate
authenticating with Globus Auth.

##DevOps

Currently the production demo app is running on an instance of the Dokku
platform. This is a Heroku like infraustructure that you can git push to deploy
on.

Full documentation can be found on the [Dokku website](http://progrium.viewdocs.io/dokku/).

###Summary of Dokku commands

The general form of commands is:

```
ssh -t dokku@AUTH_DEMO_BOX_IP <command>
```

- **Help** for a list of all commands and options

    ```
    ssh -t dokku@AUTH_DEMO_BOX_IP help
    ```

- **Rebuild production** to restart the app, as is.

    This will retrieve a fresh `client_credentials` grant request / token.

    ```
    ssh -t dokku@AUTH_DEMO_BOX_IP ps:rebuild auth_demo_prod
    ```

- **Config Variable Management**

    - To add or update a config variable (making sure to quote if necessary)

        ```
        ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod ENV_VAR_NAME="ENV_VAR_VALUE"
        ```

    - To completely remove a config variable

        ```
        ssh -t dokku@AUTH_DEMO_BOX_IP config:unset auth_demo_prod ENV_VAR_NAME
        ```


##License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
