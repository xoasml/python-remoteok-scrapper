import requests
from bs4 import BeautifulSoup


class Scrape:

    def get_page(self, keywords):

        pages = []

        for keyword in keywords:
            response = requests.get(
                f"https://remoteok.com/remote-{keyword}-jobs",
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                }
            )
            soup = BeautifulSoup(response.content, "html.parser")

            pages.append(soup.find_all("tr", class_="job"))

        return pages

    def get_jobs(self, pages):

        jobs = []

        for page in pages:

            for job in page:
                title = job.find("h2", itemprop="title")
                company = job.find("h3", itemprop="name")
                url = job.find("a", itemprop="url")["href"]
                time = job.find("time")

                tips = job.find_all("div", class_="location")
                region = tips[0].text
                salary = tips[1].text

                job_data = {
                    "company": self.formatter(company.text),
                    "title": self.formatter(title.text),
                    "region" : self.formatter(region),
                    "salary" : self.formatter(salary),
                    "url": f"https://remoteok.com{url}",
                    "time": self.formatter(time.text),
                }

                jobs.append(job_data)

        return jobs

    def formatter(self, job_data):
        return job_data.replace("\n", "").strip()



scrape = Scrape()

keywords = [
    "flutter",
    "python",
    "golang"
]

pages = scrape.get_page(keywords)
jobs = scrape.get_jobs(pages)

for job in jobs:
    print(job)
