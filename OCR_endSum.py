from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor

# Get a list of all potential "total" value 
def getTotalList(photoPath :str) -> list:
    # Can in fact open multiple image so try impliment that 
    image = Image.open(photoPath)
    langs = ["en"] # Replace with your languages - optional but recommended
    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()

    predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)

    index = 0
    totalList = []
    textList = []
    for text_line in predictions[0].text_lines:
        # Taking adavantage of the output, it is on the same line but very space out from each other
        #  then it will get output at 1 index later, here it is
        if ("total" in text_line.text.lower() ):
            totalList.append(predictions[0].text_lines[index + 1].text)

            # In case, it reads the word "total" after the value
            if (index - 1 > 0): 
                totalList.append(predictions[0].text_lines[index - 1].text)

            # Just in case, there are some weird format have the value immediately next to the total
            try:
                totalList.append(text_line.text[5:])
            except:
                continue
        index = index + 1
        totalList.append(text_line.text)
    if totalList == []:
        return text_line 
    return totalList

# Input in image that the letter on the image are horizontal
# Filter down to get the most probable total amount of the receipt
def getTotalValue (photoPath: str) -> float:
    # Get a list of all potential "total" value 
    totalList = getTotalList(photoPath)
    totalValue = []
    for total in totalList:
        try:
            # Check if "$" is in the string
            if "$" in total:
                # Find the index of "$" and convert the substring after it to float
                index = total.index("$")
                totalValue.append(float(total[index+1:]))  # Start after the "$" symbol
            else:
                # No "$" symbol, directly convert the entire string to float
                if (len(total) < 6):
                    totalValue.append(float(total))
        except:
            # Ignore any error and continue to the next item
            continue

    # In the case, there are multiple values, but if not, max would still return corrects
    return max(totalValue)

if __name__ == "__main__": 
    photoPath = input("Specified the relative path to the image: ")
    # For debugging if needed
    print(getTotalList(photoPath))
    print(getTotalValue(photoPath))


    