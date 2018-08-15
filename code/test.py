from link_crawler import link_crawler

link_crawler('http://example.webscraping.com', '/places/default/(index|view)/', delay=5, num_retries=1, max_depth=1,
             user_agent='GoodCrawler')