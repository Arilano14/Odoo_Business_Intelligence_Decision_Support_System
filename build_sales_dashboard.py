import asyncio
from playwright.async_api import async_playwright
import os
import time

ARTIFACT_DIR = r"C:\Users\Arilano\.gemini\antigravity-ide\brain\75640b5d-aee6-4ab2-81d3-a4ed10da8fd7"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--window-size=1920,1080'])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        try:
            print("Navigating to login page...")
            await page.goto('http://localhost:8070/web/login')
            
            await page.fill('input[name="login"]', 'admin')
            await page.fill('input[name="password"]', 'admin')
            await page.click('button[type="submit"]')
            
            print("Waiting for login...")
            await page.wait_for_selector('.o_main_navbar, .o_navbar', timeout=30000)
            
            print("Logged in. Navigating to Sales Pivot View...")
            await page.goto('http://localhost:8070/web#action=sale.action_orders&view_type=pivot')
            
            print("Checking for Oops modal...")
            try:
                await page.wait_for_selector('.modal-dialog:has-text("Oops!")', timeout=10000)
                print("Oops modal found! Clicking close...")
                await page.click('button:has-text("Close")')
                await asyncio.sleep(1)
            except Exception as e:
                print("No Oops modal.")
                
            try:
                await page.wait_for_selector('.modal-dialog:has-text("Missing Record")', timeout=3000)
                print("Missing Record modal found! Clicking close...")
                await page.click('button:has-text("Close")')
                await asyncio.sleep(1)
            except Exception as e:
                pass
            
            print("Waiting for Pivot View to load...")
            await page.wait_for_selector('.o_pivot', timeout=20000)
            await page.screenshot(path=os.path.join(ARTIFACT_DIR, 'step1_pivot_loaded.png'))
            
            print("Clicking 'Insert in Spreadsheet'...")
            # The button text is usually "Insert in Spreadsheet"
            await page.click('button:has-text("Insert in Spreadsheet")')
            
            print("Waiting for dialog...")
            await page.wait_for_selector('.modal-dialog', timeout=10000)
            await page.screenshot(path=os.path.join(ARTIFACT_DIR, 'step2_dialog.png'))
            
            print("Selecting 'Sales Operations' dashboard...")
            # In the dialog, we need to select the dashboard from the dropdown
            # Odoo 16/17/18 spreadsheet insertion dialog has a dropdown for the dashboard
            await page.click('.modal-body select, .modal-body input') # open dropdown
            await page.click('text="Sales Operations"')
            
            print("Clicking Confirm...")
            await page.click('button:has-text("Confirm")')
            
            print("Waiting for Spreadsheet to load...")
            await page.wait_for_selector('.o-spreadsheet', timeout=30000)
            await page.screenshot(path=os.path.join(ARTIFACT_DIR, 'step3_spreadsheet_loaded.png'))
            
            print("Saved! Exiting...")
            await asyncio.sleep(2)  # Give it a moment to save
            
        except Exception as e:
            print(f"Error occurred: {e}")
            await page.screenshot(path=os.path.join(ARTIFACT_DIR, 'error_build.png'))
            html = await page.content()
            with open(os.path.join(ARTIFACT_DIR, 'page_dump5.html'), 'w', encoding='utf-8') as f:
                f.write(html)
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
