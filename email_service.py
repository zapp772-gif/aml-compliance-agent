"""
Email service for daily compliance summaries using SendGrid
"""

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.email_address = os.getenv('EMAIL_ADDRESS')
    
    def create_html_email(self, analyzed_updates):
        """Create formatted HTML email"""
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f7fa; }}
                .container {{ max-width: 900px; margin: 0 auto; background: white; }}
                .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                          color: white; padding: 30px; }}
                .update-card {{ border-left: 4px solid #3b82f6; padding: 20px; 
                              margin: 20px; background: #f8fafc; }}
                .regulator {{ color: #1e3a8a; font-weight: 600; font-size: 14px; 
                            text-transform: uppercase; }}
                .categories {{ margin: 10px 0; }}
                .category-tag {{ display: inline-block; background: #dbeafe; color: #1e40af; 
                               padding: 4px 10px; border-radius: 12px; font-size: 11px; 
                               margin-right: 6px; margin-bottom: 6px; font-weight: 600; }}
                .title {{ color: #1e40af; font-size: 18px; font-weight: 600; margin: 10px 0; }}
                .analysis {{ line-height: 1.6; color: #334155; white-space: pre-wrap; }}
                .link {{ margin-top: 10px; }}
                .link a {{ color: #3b82f6; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AML/BSA Regulatory Update</h1>
                    <p>Daily Summary - {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
        """
        
        if not analyzed_updates:
            html_content += '<p style="text-align: center; padding: 40px;">No updates today.</p>'
        else:
            for item in analyzed_updates:
                update = item['update']
                categories = item.get('categories', [])
                
                category_tags = ''.join([f'<span class="category-tag">{cat}</span>' for cat in categories])
                
                html_content += f"""
                    <div class="update-card">
                        <div class="regulator">{item['regulator']}</div>
                        <div class="categories">{category_tags}</div>
                        <div class="title">{update.get('title', 'Update')}</div>
                        <div class="analysis">{item['analysis']}</div>
                        <div class="link"><a href="{update.get('link', '#')}">View Full Update</a></div>
                    </div>
                """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_daily_summary(self, analyzed_updates):
        """Send daily summary email using SendGrid"""
        try:
            import requests
            
            url = "https://api.sendgrid.com/v3/mail/send"
            
            headers = {
                "Authorization": f"Bearer {self.sendgrid_api_key}",
                "Content-Type": "application/json"
            }
            
            html_body = self.create_html_email(analyzed_updates)
            
            payload = {
                "personalizations": [
                    {
                        "to": [{"email": self.email_address}],
                        "subject": f"AML/BSA Compliance Update - {datetime.now().strftime('%B %d, %Y')}"
                    }
                ],
                "from": {
                    "email": self.email_address,
                    "name": "AML Compliance Agent"
                },
                "content": [
                    {
                        "type": "text/html",
                        "value": html_body
                    }
                ]
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 202:
                print(f"✓ Email sent to {self.email_address}")
                return True
            else:
                print(f"✗ Email error: {response.status_code} - {response.text}")
                return False
            
        except Exception as e:
            print(f"✗ Email error: {str(e)}")
            return False
