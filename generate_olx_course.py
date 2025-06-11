import os
import tarfile

def create_olx_course(course_id, course_name, slides_dir, output_filename="course.tar.gz"):
    """
    Creates an OLX course package from markdown slides.
    Each slide becomes an HTML component within a course unit.
    """
    
    # Base OLX structure
    olx_structure = {
        f"{course_id}/course.xml": (
            "<course url_name=\"{course_id}\" org=\"{course_id}\" course=\"{course_name}\" display_name=\"{course_name}\">\n"
            "    <chapter url_name=\"Introduction\">\n"
            "        <sequential url_name=\"Overview\">\n"
            "        </sequential>\n"
            "    </chapter>\n"
            "</course>"
        ).format(course_id=course_id, course_name=course_name),
        f"{course_id}/chapter/Introduction.xml": "<chapter display_name=\"Introduction\"/>",
        f"{course_id}/sequential/Overview.xml": "<sequential display_name=\"Overview\"/>",
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
            html_content = str(f"<!DOCTYPE html>\n<html>\n<body>\n{content.replace('\n', '<br/>')}\n</body>\n</html>")

            unit_name = f"Slide_{i}"
            html_component_name = f"slide_content_{i}"

            olx_structure[f"{course_id}/vertical/{unit_name}.xml"] = (
                "<vertical display_name=\"{unit_name}\">\n"
                "    <html url_name=\"{html_component_name}\"/>\n"
                "</vertical>"
            ).format(unit_name=unit_name, html_component_name=html_component_name)
            
            olx_structure[f"{course_id}/html/{html_component_name}.xml"] = (
                "<html display_name=\"{unit_name}\">\n"
                "    <div markdown=\"1\">\n"
                "        {html_content}\n"
                "    </div>\n"
                "</html>"
            ).format(unit_name=unit_name, html_content=html_content)
            
            html_unit_refs.append("<vertical url_name=\"{unit_name}\"/>".format(unit_name=unit_name))

    # Update sequential with unit references
    olx_structure[f"{course_id}/sequential/Overview.xml"] = (
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

    print(f"OLX course '{course_name}' created as {output_filename}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    create_olx_course(
        course_id="BoostMeUp-LMS-PoC",
        course_name="Boost Me Up LMS PoC Presentation",
        slides_dir=current_dir,
        output_filename="boost_me_up_poc_course.tar.gz"
    ) 