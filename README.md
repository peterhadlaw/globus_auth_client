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


##Setup Service

1. Start with a fresh, organic, free range Ubuntu 14.04 x64 machine.

2. Setup the Dokku platform

     - SSH (as "ubuntu" for example on AWS) and run the following:

       ```
       wget https://raw.githubusercontent.com/progrium/dokku/v0.4.3/bootstrap.sh
       sudo DOKKU_TAG=v0.4.3 bash bootstrap.sh
       ```

3. Add your SSH key as a Dokku deploy key

   ```
    cat ~/.ssh/id_rsa.pub | ssh <root_user>@AUTH_DEMO_BOX_IP "sudo sshcommand acl-add dokku globus"
    ```

4. Create app on the platform and set configuration variables

   ```
   ssh -t dokku@AUTH_DEMO_BOX_IP apps:create auth_demo_prod
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod 
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod CREDENTIAL_SCOP_ID="auth:login"
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod DEBUG="False"
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod FLASK_ENV="production"
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod OAUTH_CLIENT_ID="<OAUTH_CLIENT_ID>"
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod OAUTH_CLIENT_SECRET="<OAUTH_CLIENT_SECRET>"
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod SCOPE_ID="auth:view_identities"
   ssh -t dokku@AUTH_DEMO_BOX_IP config:set auth_demo_prod SECRET_APPLICATION_KEY="<secure_random_key>"
   ```

5. Deploy this app to the Dokku platform

   From within a cloned copy of this git repo, run the following:

   ```
   git remote add dokku dokku@AUTH_DEMO_BOX_IP:auth_demo_prod
   git push dokku master
   ```

   There will be `remote:` output, towards the end of this output, the active url will show.
   It will be along the lines of: `http://auth_demo_prod.AUTH_DEMO_BOX_DNS`

6. Adjust your DNS accordingly to point to the Dokku box and update the app url:

   ```
   ssh -t dokku@AUTH_DEMO_BOX_IP domains:add auth_demo_prod http://production.url
   ```

7. Setup the SSL layer


##License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
