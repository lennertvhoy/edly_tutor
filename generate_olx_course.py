import os
import tarfile
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text

def create_olx_course(course_id_org, course_id_number, course_display_name, slides_dir, output_filename="course.tar.gz"):
    """
    Creates an OLX course package from markdown slides.
    Each slide becomes an HTML component within a course unit.
    """
    
    course_id_run = slugify(course_display_name)
    
    full_course_key_string = f"{course_id_org}/{course_id_number}/{course_id_run}"

    # Base OLX structure
    olx_structure = {
        f"{course_id_org}/{course_id_number}/{course_id_run}/course.xml": (
            "<course url_name=\"{course_id_run}\" org=\"{course_id_org}\" course=\"{course_id_number}\" display_name=\"{course_display_name}\">\n"
            "    <chapter url_name=\"introduction\">\n"
            "        <sequential url_name=\"overview\">\n"
            "        </sequential>\n"
            "    </chapter>\n"
            "</course>"
        ).format(
            course_id_org=course_id_org,
            course_id_number=course_id_number,
            course_id_run=course_id_run,
            course_display_name=course_display_name
        ),
        f"{course_id_org}/{course_id_number}/{course_id_run}/chapter/introduction.xml": "<chapter display_name=\"Introduction\"/>",
        f"{course_id_org}/{course_id_number}/{course_id_run}/sequential/overview.xml": "<sequential display_name=\"Overview\"/>",
    }

    # Read slide content and create OLX HTML components
    slide_count = 0
    html_unit_refs = []
    
    for i in range(1, 7): # Assuming slides from slide1.md to slide6.md
        slide_filename = os.path.join(slides_dir, f"slide{i}.md")
        if os.path.exists(slide_filename):
            slide_count += 1
            with open(slide_filename, "r") as f:
                content = f.read()
            
            # Convert markdown to basic HTML for OLX.
            # This is a very basic conversion; for complex markdown, consider a library.
            html_content = (
                "<!DOCTYPE html>\n<html>\n<body>\n"
                f"{content.replace('\n', '<br/>')}\n"
                "</body>\n</html>"
            )

            unit_name_slug = slugify(f"Slide {i}")
            html_component_name_slug = slugify(f"Slide Content {i}")

            olx_structure[f"{course_id_org}/{course_id_number}/{course_id_run}/vertical/{unit_name_slug}.xml"] = (
                "<vertical display_name=\"Slide {i}\">\n"
                "    <html url_name=\"{html_component_name_slug}\"/>\n"
                "</vertical>"
            ).format(i=i, html_component_name_slug=html_component_name_slug)
            
            olx_structure[f"{course_id_org}/{course_id_number}/{course_id_run}/html/{html_component_name_slug}.xml"] = (
                "<html display_name=\"Slide {i}\">\n"
                "    <div markdown=\"1\">\n"
                "        {html_content}\n"
                "    </div>\n"
                "</html>"
            ).format(i=i, html_content=html_content)
            
            html_unit_refs.append("<vertical url_name=\"{unit_name_slug}\"/>".format(unit_name_slug=unit_name_slug))

    # Update sequential with unit references
    olx_structure[f"{course_id_org}/{course_id_number}/{course_id_run}/sequential/overview.xml"] = (
        "<sequential display_name=\"Overview\">\n"
        "    {html_unit_refs_joined}\n"
        "</sequential>"
    ).format(html_unit_refs_joined=''.join(html_unit_refs))

    # Create the tar.gz archive
    with tarfile.open(output_filename, "w:gz") as tar:
        for name, content in olx_structure.items():
            # Create a dummy file in a temp directory to add to the tar
            temp_filepath = os.path.join("/tmp", name)
            os.makedirs(os.path.dirname(temp_filepath), exist_ok=True)
            with open(temp_filepath, "w") as f:
                f.write(content)
            tar.add(temp_filepath, arcname=name)
            os.remove(temp_filepath) # Clean up temp file

    print(f"OLX course '{course_display_name}' created as {output_filename}")
    print(f"Full Course ID for import and shell access: {full_course_key_string}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    create_olx_course(
        course_id_org="BoostMeUp", 
        course_id_number="LMS-PoC", 
        course_display_name="Boost Me Up LMS PoC Presentation",
        slides_dir=current_dir,
        output_filename="boost_me_up_poc_course.tar.gz"
    ) 