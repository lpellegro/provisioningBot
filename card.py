from credentials import credentials
#this card allows the admin to authenticate to Webex
oauthUrl = credentials["oauth_authorization_url"]

def card ():


        card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.2",
            "body": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "220px",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "AUTHENTICATION",
                                    "wrap": True,
                                    "size": "ExtraLarge",
                                    "fontType": "Monospace"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "REQUIRED",
                                    "wrap": True,
                                    "size": "ExtraLarge",
                                    "fontType": "Monospace"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "ImageSet",
                                    "images": [
                                        {
                                            "type": "Image",
                                            "size": "Large",
                                            "url": "https://www.cisco.com/c/en/us/products/conferencing/webex/jcr:content/Grid/category_atl_6b9a/layout-category-atl/blade/bladeContents3/tile/image.img.png/1590697890585.png"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "TextBlock",
                    "text": "Make sure your device can reach the internal server handling the bot",
                    "wrap": True,
                    "separator": True,
                    "size": "Small",
                    "fontType": "Monospace"
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "stretch",
                            "items": [
                                {
                                    "type": "ActionSet",
                                    "horizontalAlignment": "Center",
                                    "actions": [
                                        {
                                            "type": "Action.OpenUrl",
                                            "title": "Authenticate",
                                            "url": oauthUrl
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return card
