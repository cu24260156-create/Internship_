
"""
Internship Domain Recommendation Engine
---------------------------------------
Algorithm: Content-Based Filtering + Weighted Scoring
Dependencies: Python 3.x standard library only
"""

from dataclasses import dataclass
from typing import List, Set


# -------------------- INTERNSHIP DATASET --------------------

@dataclass
class InternshipDomain:
    name: str
    skills: Set[str]
    interests: Set[str]
    min_education: int
    work_modes: Set[str]
    description: str
    careers: List[str]


DOMAINS = [
    InternshipDomain(
        "Web Development",
        {"html", "css", "javascript", "python", "react", "sql"},
        {"websites", "frontend", "backend", "design", "programming"},
        1, {"remote", "onsite", "hybrid"},
        "Build and maintain websites and web applications.",
        ["Frontend Developer", "Backend Developer", "Full Stack Developer"]
    ),
    InternshipDomain(
        "Artificial Intelligence / Machine Learning",
        {"python", "machine learning", "statistics", "numpy", "pandas"},
        {"ai", "automation", "research", "prediction", "robotics"},
        2, {"remote", "onsite", "hybrid"},
        "Develop intelligent systems and predictive models.",
        ["ML Engineer", "AI Engineer", "Research Engineer"]
    ),
    InternshipDomain(
        "Data Science",
        {"python", "sql", "statistics", "excel", "pandas", "power bi"},
        {"analytics", "visualization", "business", "research", "prediction"},
        1, {"remote", "onsite", "hybrid"},
        "Analyze data to discover patterns and support decisions.",
        ["Data Analyst", "Data Scientist", "BI Analyst"]
    ),
    InternshipDomain(
        "Cybersecurity",
        {"networking", "linux", "python", "security", "cryptography"},
        {"security", "ethical hacking", "privacy", "investigation"},
        2, {"remote", "onsite", "hybrid"},
        "Protect computer systems, networks, and information.",
        ["Security Analyst", "Penetration Tester", "SOC Analyst"]
    ),
    InternshipDomain(
        "Cloud Computing / DevOps",
        {"linux", "docker", "aws", "networking", "python", "git"},
        {"automation", "infrastructure", "deployment", "cloud", "servers"},
        2, {"remote", "onsite", "hybrid"},
        "Deploy applications and manage cloud infrastructure.",
        ["Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer"]
    ),
    InternshipDomain(
        "UI/UX Design",
        {"figma", "wireframing", "prototyping", "html", "css"},
        {"design", "creativity", "user experience", "art", "websites"},
        1, {"remote", "onsite", "hybrid"},
        "Design user-friendly and visually appealing digital products.",
        ["UI Designer", "UX Designer", "Product Designer"]
    ),
    InternshipDomain(
        "Mobile App Development",
        {"java", "kotlin", "swift", "flutter", "dart", "python"},
        {"mobile apps", "android", "ios", "programming", "design"},
        1, {"remote", "onsite", "hybrid"},
        "Create applications for smartphones and tablets.",
        ["Android Developer", "iOS Developer", "Mobile App Developer"]
    ),
    InternshipDomain(
        "Digital Marketing",
        {"seo", "content writing", "analytics", "social media", "excel"},
        {"marketing", "communication", "advertising", "creativity", "business"},
        1, {"remote", "onsite", "hybrid"},
        "Promote brands using digital channels and campaigns.",
        ["SEO Specialist", "Marketing Analyst", "Content Strategist"]
    ),
    InternshipDomain(
        "Blockchain Development",
        {"solidity", "javascript", "python", "cryptography", "git"},
        {"blockchain", "security", "web3", "programming", "finance"},
        2, {"remote", "onsite", "hybrid"},
        "Develop decentralized applications and smart contracts.",
        ["Blockchain Developer", "Smart Contract Engineer"]
    ),
    InternshipDomain(
        "Business Analysis",
        {"excel", "sql", "power bi", "statistics", "communication"},
        {"business", "analytics", "problem solving", "research", "planning"},
        1, {"remote", "onsite", "hybrid"},
        "Use data and business requirements to improve processes.",
        ["Business Analyst", "Product Analyst", "Operations Analyst"]
    ),
]


# -------------------- USER PROFILE --------------------

EDUCATION_LEVELS = {
    "diploma": 1,
    "bachelor": 2,
    "master": 3,
    "phd": 4
}


def get_profile():
    print("\n" + "=" * 55)
    print("     INTERNSHIP DOMAIN RECOMMENDATION ENGINE")
    print("=" * 55)

    name = input("\nEnter your name: ").strip() or "Student"

    print("\nEducation levels:")
    print("1. Diploma / Beginner")
    print("2. Bachelor's degree")
    print("3. Master's degree")
    print("4. PhD")

    while True:
        education = input("Select education level (1-4): ").strip()
        if education in {"1", "2", "3", "4"}:
            education = int(education)
            break
        print("Please enter a number from 1 to 4.")

    skills = {
        item.strip().lower()
        for item in input(
            "\nEnter your skills (comma-separated): "
        ).split(",") if item.strip()
    }

    interests = {
        item.strip().lower()
        for item in input(
            "Enter your interests (comma-separated): "
        ).split(",") if item.strip()
    }

    print("\nPreferred work mode:")
    print("1. Remote")
    print("2. Onsite")
    print("3. Hybrid")
    print("4. Any")

    modes = {"1": "remote", "2": "onsite", "3": "hybrid"}

    while True:
        choice = input("Choose an option (1-4): ").strip()
        if choice in {"1", "2", "3", "4"}:
            work_mode = modes.get(choice, "any")
            break
        print("Please enter a number from 1 to 4.")

    return {
        "name": name,
        "education": education,
        "skills": skills,
        "interests": interests,
        "work_mode": work_mode
    }


# -------------------- FILTERING ALGORITHM --------------------

def recommend_domains(profile):
    results = []

    # Step 1: Filter domains by education eligibility.
    eligible = [
        domain for domain in DOMAINS
        if profile["education"] >= domain.min_education
    ]

    # Step 2: Apply the preferred work-mode filter.
    # If no domain supports the requested mode, retain eligible domains.
    if profile["work_mode"] != "any":
        mode_filtered = [
            domain for domain in eligible
            if profile["work_mode"] in domain.work_modes
        ]
        if mode_filtered:
            eligible = mode_filtered

    # Step 3: Calculate weighted content-based similarity.
    for domain in eligible:
        matched_skills = profile["skills"] & domain.skills
        matched_interests = profile["interests"] & domain.interests

        # Skill match: 50% of the total score.
        skill_score = (
            len(matched_skills) / len(domain.skills) * 50
            if domain.skills else 0
        )

        # Interest match: 30% of the total score.
        interest_score = (
            len(matched_interests) / len(domain.interests) * 30
            if domain.interests else 0
        )

        # Education eligibility: 10% of the total score.
        education_score = 10

        # Work-mode compatibility: 10% of the total score.
        mode_score = (
            10 if profile["work_mode"] == "any"
            or profile["work_mode"] in domain.work_modes
            else 0
        )

        total_score = (
            skill_score + interest_score
            + education_score + mode_score
        )

        results.append({
            "domain": domain,
            "score": round(min(total_score, 100), 2),
            "skills": matched_skills,
            "interests": matched_interests
        })

    # Step 4: Rank domains from highest to lowest score.
    results.sort(key=lambda item: item["score"], reverse=True)

    # Step 5: Recommend domains with at least one profile match.
    matched = [
        result for result in results
        if result["skills"] or result["interests"]
    ]

    return matched if matched else results


# -------------------- DISPLAY RECOMMENDATIONS --------------------

def display_recommendations(profile, results):
    print("\n" + "=" * 55)
    print(f"RECOMMENDATIONS FOR {profile['name'].upper()}")
    print("=" * 55)

    if not results:
        print("No eligible domains found.")
        return

    for rank, item in enumerate(results[:5], start=1):
        domain = item["domain"]

        print(f"\n{rank}. {domain.name}")
        print(f"   Match score: {item['score']}%")
        print(f"   Description: {domain.description}")

        print(
            "   Matched skills: "
            + (", ".join(sorted(item["skills"])) or "None yet")
        )

        print(
            "   Matched interests: "
            + (", ".join(sorted(item["interests"])) or "None yet")
        )

        print("   Potential careers: " + ", ".join(domain.careers))

        if item["score"] >= 50:
            print("   Recommendation: Strong profile match")
        elif item["score"] >= 25:
            print("   Recommendation: Moderate profile match")
        else:
            print("   Recommendation: Explore and build relevant skills")

    print("\n" + "=" * 55)
    print("Tip: Learn missing skills and build projects to improve")
    print("your suitability for your preferred internship domain.")
    print("=" * 55)


# -------------------- MAIN PROGRAM --------------------

def main():
    while True:
        profile = get_profile()
        recommendations = recommend_domains(profile)
        display_recommendations(profile, recommendations)

        again = input(
            "\nCreate another recommendation? (y/n): "
        ).strip().lower()

        if again != "y":
            print("\nThank you for using the recommendation engine!")
            break


if __name__ == "__main__":
    main()