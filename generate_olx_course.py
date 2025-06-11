import os
import tarfile
import re
import subprocess
import shutil

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text

def rework_content_with_ai_concept(original_markdown_content: str) -> str:
    """
    Conceptual placeholder function to simulate AI-driven content reworking.
    In a real scenario, this would involve calling an AI API (e.g., OpenAI GPT-4, Cursor AI)
    to reformat, standardize, segment, or prepare content for translation.
    
    For this proof-of-concept, it will simply indicate where AI processing would occur.
    """
    # Simulate AI processing by adding a note (or perform simple text manipulation)
    reworked_content = f"\n{{{{AI_REWORKED_CONTENT_START}}}}\n\n" \
                       f"[AI Rewritten]: Original content follows: {original_markdown_content}" \
                       f"\n\n{{{{AI_REWORKED_CONTENT_END}}}}\n"
    return reworked_content

def create_olx_course_from_structured_markdown(
    course_id_org,
    course_id_number,
    course_display_name,
    structured_markdown_filepath,
    output_filename="course.tar.gz"
):
    """
    Creates an OLX course package from a single structured markdown file using mu-courses.
    """
    course_id_run = slugify(course_display_name)
    full_course_key_string = f"{course_id_org}/{course_id_number}/{course_id_run}"

    temp_olx_output_dir = "temp_olx_output"
    
    try:
        # 1. Run mu to convert structured markdown to OLX directory
        os.makedirs(temp_olx_output_dir, exist_ok=True)

        print(f"Converting {structured_markdown_filepath} to OLX using mu-courses...")
        mu_command = ["mu", structured_markdown_filepath, temp_olx_output_dir]
        subprocess.run(mu_command, check=True, capture_output=True, text=True)
        print("mu-courses conversion complete.")

        # 2. Create the tar.gz archive directly from the generated OLX contents
        # Mu places the OLX files directly in the specified output directory.
        with tarfile.open(output_filename, "w:gz") as tar:
            # Add all contents of the generated OLX directory directly to the tarball root
            # This ensures course.xml is at the root of the extracted tar, which Open edX expects.
            for item in os.listdir(temp_olx_output_dir):
                item_path = os.path.join(temp_olx_output_dir, item)
                # The arcname=item makes sure the item is added to the root of the tarball
                tar.add(item_path, arcname=item)
        
        print(f"OLX course '{course_display_name}' created as {output_filename}")
        print(f"Full Course ID for import and shell access: {full_course_key_string}")

    except subprocess.CalledProcessError as e:
        print(f"Error running mu-courses: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise

def generate_structured_markdown_from_slides(
    slides_dir,
    course_id_org,
    course_id_number,
    course_display_name
):
    """
    Generates a single structured Markdown file suitable for mu-courses
    from individual slide markdown files (slide1.md to slide6.md).
    """
    structured_md_content = []
    
    # Add top-level course metadata for mu, using olx-url_name for the course run name
    course_url_name = slugify(course_display_name)
    structured_md_content.append(f"# {course_display_name} {{olx-org=\"{course_id_org}\" olx-course=\"{course_id_number}\" olx-url_name=\"{course_url_name}\"}}")
    
    # Explicitly define chapter and sequential with olx-type
    structured_md_content.append(f"\n## Introduction {{olx-type=\"chapter\"}}")
    structured_md_content.append(f"\n### Overview {{olx-type=\"sequential\"}}")

    for i in range(1, 7): # Iterate through assumed slides from slide1.md to slide6.md
        slide_filename = os.path.join(slides_dir, f"slide{i}.md")
        if os.path.exists(slide_filename):
            with open(slide_filename, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            # --- AI Reworking Step (Conceptual) ---
            reworked_content = rework_content_with_ai_concept(original_content)
            # -------------------------------------

            # Each slide becomes a unit (vertical) under the sequential
            structured_md_content.append(f"\n#### Slide {i} Content {{olx-type=\"vertical\"}}")
            structured_md_content.append(reworked_content)
            structured_md_content.append("") # Ensure a newline after content

    temp_structured_md_filepath = "structured_course_temp.md"
    with open(temp_structured_md_filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(structured_md_content))
    
    return temp_structured_md_filepath

if __name__ == "__main__":
    current_dir = os.getcwd() # Assumes slide*.md are in the current directory
    
    # Define course details
    course_org = "BoostMeUp"
    course_number = "LMS-PoC"
    course_title = "Boost Me Up LMS PoC Presentation"
    output_tar_filename = "boost_me_up_poc_course_mu.tar.gz" # Changed output name to distinguish

    # Generate the structured markdown file
    structured_md_file = generate_structured_markdown_from_slides(
        current_dir,
        course_org,
        course_number,
        course_title
    )

    try:
        # Create the OLX package using the new function with mu-courses
        create_olx_course_from_structured_markdown(
            course_org,
            course_number,
            course_title,
            structured_md_file,
            output_tar_filename
        )
    finally:
        # Clean up the temporary structured markdown file
        if os.path.exists(structured_md_file):
            os.remove(structured_md_file) 