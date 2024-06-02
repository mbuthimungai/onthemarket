import asyncio
from queue import Queue
import math
import random
from scrapers.scrapers import OnTheMarket


async def call_fill_form_script(contact_form_url: str, custom_message: str, delay: int) -> str:
    script_path = './scrapers/send_email.js'  # Replace with the actual path to fill_form.js
    process = await asyncio.create_subprocess_exec(
        'node', script_path, contact_form_url, custom_message, str(delay),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    
    # Check if the process exit code indicates success(True) or failure(False)    
    if process.returncode == 0:
        return True
    else:
        return False

async def search_properties(url: str, custom_message: str, delay: str):
    on_the_market = OnTheMarket()
    total_results = await on_the_market.extract_total_number_properties(url=url)
    
    results_per_page = 24
    print("total_results", total_results)
    number_of_pages = math.ceil(total_results / results_per_page)
    for i in range(1, number_of_pages + 1):
        
        if i > 42:
            break
        
        url = f'{url}?page={i}'
        contact_form_links = await on_the_market.extract_contact_form_links(url)
        
        random_wait_time = random.randint(3, 7)
        for contact_form_link in contact_form_links:
            
            await asyncio.sleep(random_wait_time)            
            await call_fill_form_script(contact_form_url=contact_form_link, 
                                        custom_message=custom_message, delay=100)

async def process_queue(queue: Queue):
    while True:
        url, custom_message, delay = queue.get()
        on_the_market = OnTheMarket()
        await on_the_market.extract_user_agents(url='https://www.useragents.me/')
        await search_properties(url, custom_message, delay)
        queue.task_done()
        if queue.empty():
            await asyncio.sleep(1)  # Small sleep to prevent busy waiting
            
            

