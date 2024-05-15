import os
import torch
import gc
from diffusers import StableDiffusionPipeline

import pandas as pd


# Set CUDA environment variables (optional)

print(torch.cuda.is_available())

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
# Clear CUDA cache (optional)
gc.collect()
torch.cuda.empty_cache()

# Load pretrained model
#model_name = "stablediffusionapi/picxreal"
model_name = "stabilityai/stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float32)
pipe = pipe.to("cuda")
pipe.safety_checker = None

real_news= ["Erdogan risks losing power as Turkey’s high-stakes election reaches its climax",

"Erdogan's rival boosted by withdrawal, poll lead ahead of Turkey vote",

"US Military Could Lose Space Force Trademark to Netflix Series",

"White House threatens to fire anyone who tries to quit",

"United States Risks Sanctions From Zimbabwe If Elections Are Not Free And Fair",

"Trump was ‘not wrong’ when he warned criminals are coming across US border: Tom Homan",

"Trump promotes ‘God Bless the USA’ Bible",

"Rapper 50 Cent admits he thinks Trump’s ‘gonna be president again",

"Hillary Clinton warns AI tech will make 2016 election disinformation 'look primitive'",

"Microsoft says a Russian hacking group is still trying to crack into its systems"]

fake_news=[

"Exclusive: Erdogan Caught Photoshopping Extra Crowds into His Rally Pictures for 'More Impact’",

"Turkey's Education System Under Scrutiny: Critics Accuse Erdogan's Government of Ideological Agenda",

"Drunk man accidentally takes $1,600 Uber from West Virginia to New Jersey",

"SNL star, Donald Trump Jr-Aubrey O'Day cheating scandal resurface",

"Man contracts rare infection likely during cockroach-related activities, confirmed in China",

"Levin: Biden has unleashed a housing apocalypse on America as Americans scramble to move out of cities",

"NYC's $2,000 Fine for Posting a ‘Hate Speech' Sign set off a  Supreme Court debate on anti-bias laws",

"Up to 36 million vote-by-mail ballots could go missing in 2020, a new study says",

"Madonna predicted the COVID-19 outbreak in creepy bath video: ‘It’s the great equalizer’",

"Sweden bans balloons from Royal Wedding 'due to the environmental impact'",

"NYC voters waking up to find presidential ballot error that could cost Biden votes on local races",

"Biden suffers another major legal defeat in fight over weakened ICE deportations",

]

# Define parameters
h = 584
w = 584
steps = 100
guidance = 20
#negative_prompt = "easynegative, logo, lowres, bad anatomy, ..."
negative_prompt = ""


# Generate image
'''''''''
counter = 1
for elem in fake_news:

    prompt =  elem
    print(prompt)
    image = pipe(prompt, height=h, width=w, num_inference_steps=steps, guidance_scale=guidance, negative_prompt=negative_prompt).images[0]

# Save image
    image.save("f"+str(counter)+".jpg")
    counter+=1
'''''''''

####
df1 = pd.read_csv('gpt_combined.csv', header=None, names=['Column1', 'Column2'])

for index, row in df1.iterrows():
    prompt = row['Column1']
    id_ = row['Column2']
    print(prompt, id_)
    image = pipe(prompt, height=h, width=w, num_inference_steps=steps, guidance_scale=guidance, negative_prompt=negative_prompt).images[0]
# Save image
    image.save("f"+str(id_)+".jpg")

df2 = pd.read_csv('real_combined.csv', header=None, names=['Column1', 'Column2'])

for index, row in df2.iterrows():
    prompt = row['Column1']
    id_ = row['Column2']
    print(prompt, id_)
    image = pipe(prompt, height=h, width=w, num_inference_steps=steps, guidance_scale=guidance,
                 negative_prompt=negative_prompt).images[0]
    # Save image
    image.save("r" + str(id_) + ".jpg")


