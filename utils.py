import re

def extract_json_blocks(text):
    pattern = r'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(pattern, text, re.MULTILINE)
    if len(matches) != 0:
        return matches[0]
    else:
        return text
    
def remove_trailing_commas(json_string):
    # Remove trailing commas from arrays
    json_string = re.sub(r',\s*\]', ']', json_string, flags=re.MULTILINE)
    # Remove trailing commas from objects
    json_string = re.sub(r',\s*}', '}', json_string, flags=re.MULTILINE)
    return json_string  

if __name__ == "__main__":
    test = """```json
[
  {
    "question": "How do I turn on my device?",
    "answer": "To turn on the device, press and hold the power button located on the top right corner for 3 seconds until the screen lights up."
  },
  {
    "question": "What is the battery life of my product?",
    "answer": "The battery life of this product is approximately 8 hours with normal usage. This can vary depending on the settings and applications used."
  },
  {
    "question": "How do I connect my device to Wi-Fi?",
    "answer": "To connect to Wi-Fi, go to Settings > Network > Wi-Fi, turn on Wi-Fi, select your network from the list, and enter the password when prompted."
  },
  {
    "question": "What are the different washing cycles available in this machine?",
    "answer": "The washing machine offers various cycles such as Normal, Eco, Intensive, Delicate, Quick Wash, and Spin Only. These cycles cater to specific fabric types and wash intensities."
  },
  {
    "question": "How do I adjust the water level on the machine?",
    "answer": "Adjusting the water level can be done by selecting the desired amount from the settings menu in the control panel, usually marked as 'Water Level' or similar." 
  },
  {
    "question": "What type of detergent is best for this washing machine?",
    "answer": "While the manual provides general guidance, using high-efficiency detergent for this appliance is recommended to ensure optimal performance and energy savings."
  },
  {
    "question": "How do I remove lint from inside the washing machine?",
    "answer": "To remove lint, you can utilize the lint filter provided. Refer to your user manual for its location and proper cleaning instructions."
  }
]
```"""
    test_2 = "['hello']"
    
    test_3 ="""[
  {
    "question": "How do I turn on my washing machine?",
    "answer": "To start a wash cycle, press the power button located on the control panel."
  },
  {
    "question": "What type of detergent is best for my machine?",
    "answer": "The best detergent for your machine depends on its specific settings and cycles. Check your owner's manual for guidance. Consider using a high-efficiency (HE) detergent for optimal cleaning."
  },
  {
    "question": "How do I load laundry into the washing machine?",
    "answer": "Load clothes gently, ensuring they are not clumped together, and avoid overloading the drum. Leave some space at the top of the drum to allow for proper water circulation and air flow."
  },
  {
    "question": "What does the error code 'F1' mean?",
    "answer": "An 'F1' error code typically indicates a drainage issue.  Ensure that the hose connecting to your drainage system is clear and properly connected."
  },
  {
    "question": "How often should I clean my washing machine?",
    "answer": "Clean your washing machine regularly, using a suitable cleaner for removing detergent residue and hard water stains. Follow manufacturer instructions and aim for at least every 1-2 months of use to ensure optimal performance."
  },
  {
    "question": "Can I wash delicate fabrics in the washing machine?",
    "answer": "Yes, you can often wash delicate items in your washing machine. Use a low water level, gentle cycle, and select the appropriate setting for delicate garments. Always check the care label."
  },
  {
    "question": "How do I adjust the spin speed on my washing machine?",
    "answer": "Spin speed is typically controlled through a dial or button on the control panel. Consult your owner's manual for specific instructions."
  },
  {
    "question": "Where can I find troubleshooting tips for my machine?",
    "answer": "You can find detailed troubleshooting information in the user manual, including common problem areas and solutions."
  },
]"""    
    print(extract_json_blocks(test))
    print(extract_json_blocks(test_2))
    print(remove_trailing_commas(test_3))