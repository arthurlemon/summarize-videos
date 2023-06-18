## Backend
- [ ] Summarization: Add check on token length to summarize whole transcript for overall summary (vs. summary of section summaries)
- [ ] Speed: Call openai async to accelerate process (currently 30s to 1min for rendering for a 20min video, aim at 5s)
- [ ] Add config to summatize in en or fr
- [ ] Data: Use DB instead of json for data storing
- [ ] Analyze full playlists, leveraging [youtube python api](https://pypi.org/project/python-youtube/)
- [ ] Extract info from transcript other than high-level summary (prompt engineering)
- [ ] Scrape youtube for a specific person company to extract info on their videos / needs

## Frontend
- [ ] Add full transcript under a "See original transcript" button
