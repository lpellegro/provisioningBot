#CREDENTIALS: includes installation-specific items. Some variables are critical. For those that are considered to be critical such as passwords, link these variables to environment variables
#i.e. make "ad_password" an evironment variable

credentials = { #WEBEX BOT SETTINGS
               "bearer": "your_bot_access_token",
               "botPersonId": "your_bot_id",
               "botEmail": "your_bot_username/email",
               "wl_dom": ["example1.com", "example2.com", "example3.com"], #Domain whitelist for the bot. Only those who login in Webex using those domains can add and query the bot. You can add more domains to the list
               #UCM SECTION
               "username": "ucmadmin", #ucm username, password and host
               "password": "ucmpassword",
               "host": "ucmipaddress",
               "partition": "default_partition", #default partition if partition is not specified in the provisioning file
               "css": "default_calling_search_space", #default css if css is not specified in the provisioning file
               "device_pool": "default_device_pool", #default device pool if d.p. is not specified in the provisioning file
               "sip_profile": "default_sip_profile", #default sip profile if s.p. is not specified in the provisioning file
               "location": "Hub_None", #default UCM location if is not specified in the provisioning file
	           "wsdl": "/home/admin/provisioning/AXL/schema/12.5/AXLAPI.wsdl", #filename and path to your AXL schema
               "path": "/home/admin/contacts/files", #path to a local folder where provisioning files and contact files are stored
               #WEBEX ORG SECTION
               "webexUrl": "https://webexapis.com/v1/",
               "org_url": "https://webexapis.com/v1/organizations",
               "people_url": "https://webexapis.com/v1/people/",
               "user_details_url": "https://webexapis.com/v1/people?email=",
               "location_id_url": "https://webexapis.com/v1/locations",
               "main_location": "SJC", #default Webex org location if location is not specified in the provisioning file
               "license_url": "https://webexapis.com/v1/licenses",
               #WEBEX INTEGRATION SETTINGS
               "client_id": "your_webex_integration_client_id",
               "client_secret": "your_webex_client_secret",
               "oauth_authorization_url": "your_oauth_authorization_url",
               "redirect_uri": "your_redirect_uri", # use http://localhost:<port_number> for your local machine or the internal IP of the server running the script
               "integration_id": "your_integration_id",
               #ACTIVE DIRECTORY SECTION
               "ad_ip": "10.189.105.56",
               "ad_admin": "cn=your_admin_username, cn=Users,dc=yourdomain,dc=com", #replace with the user"s AD path
               "ad_password": "ad_read_and_write_password",
               "search_base": "cn=Users,dc=yourdomain,dc=com", #replace with the search base
               #AMAZON WORKMAIL SECTION
               "aws_region_name": "your_aws_region_name",
               "domain": "cloudentpa.com",  # email domain
               "aws_access_key_id": "your_aws_access_key",
               "aws_secret_access_key": "your_aws_secret_key",
               "aws_organization_id": "your_aws_org_id",
               #ALL SECTIONS
               "user_default_password": "default_password_for_users" #AD, email, Webex, DI/unified CM user"s default password
               }
