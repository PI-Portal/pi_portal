# Setting Up Your Slack Bot

You'll need to create a Slack App in order to use pi_portal, fortunately it's not that difficult.

Step 1: Initial App Creation
- Head to: [https://api.slack.com/apps/](https://api.slack.com/apps/)
- Click on "Create New App".
- Choose "From Scratch".
- Give your app an appropriate name, we're partial to "pi_portal".
- Select your workspace from the dropdown.
- Press the "Create App" button.

Step 2: The "Signing Secret"
- You'll be redirected to your app's "Basic Configuration" screen.
- Scroll down and find the "Signing Secret".
- Copy and paste it into your pi_portal configuration for the key marked "SLACK_APP_SIGNING_SECRET".

Step 3: Enable Socket Mode, and get your "App-Level Token"
- Select "Socket Mode" from the menu of the left side of the screen.
- Click on the button "Enable Socket Mode".
- You'll be prompted to an "App-Level Token", with the "connections:write" permission. We need this.
- Give your token a name (i.e. "pi_portal App Token"), generate it, and copy and paste its value into your pi_portal configuration for the key marked "SLACK_APP_TOKEN".

Step 4: Setup "Bot Token Scopes"
- Select "OAuth & Permissions" from the menu of the left side of the screen.
- Scroll down to the "Bot Token Scopes" section, we're going to add some scopes:
  - "channels:history" will allow your bot to read messages on public channels it's been invited to.
  - "chat:write" allows your bot to send messages.
  - "files:write" allows your bot to upload images and videos.
  - "groups:history" will allow your bot to read messages on private channels it's been invited to.
- This should be sufficient for everyday usage.

Step 5: Setup "Enable Events"
- Select "Event Subscriptions" from the menu on the left side of the screen.
- Click the button to "Enable Events".
- Inside the "Subscribe to bot events" section, we need to enable a couple of events:
  - "message.channels" will allow our bot to react to new messages in public channels it's been invited to.
  - "message.groups" will allow your bot to react to new messages on private channels it's been invited to.

Step 6: Install the App to your Workspace
- Select "Install App" from the menu of the left side of the screen.
- Press the button marked "Install to Workspace".
- Confirm the permissions, and then press the "Allow" button.
- You'll receive a "Bot User OAuth Token" if successful.
- Copy and paste it into your pi_portal configuration for the key marked "SLACK_BOT_TOKEN".

Step 7: Invite Your Bot to the Channel you wish to use
- Go to the Slack app proper, and select "View Channel Details" on the channel you wish to add the bot too.
- Select the "Integrations" tab, and "add apps".
- Select your app from the drop-down menu and click its "Install" button.
- Select the "About" tab and at the bottom you'll find the channel's "Slack ID".
- Copy and paste it into your pi_portal configuration for the key marked "SLACK_CHANNEL_ID".
- While you're at it, update your pi_portal configuration for the key marked "SLACK_CHANNEL" with the regular name of your channel.
