from app.services.summary import generate_summary

transcript = """
Today we discussed artificial intelligence,
startups,
fundraising,
and scaling engineering teams.
"""

print(
    generate_summary(transcript)
)