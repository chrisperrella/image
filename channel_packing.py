import json
from pathlib import Path
from PIL import Image, ImageColor
from threading import Thread

def get_material_configs():
	material_config_path = Path( Path(__file__).parent.absolute(), 'materials')
	material_configs = list()
	for config in material_config_path.iterdir():
		if config.suffix == '.json':
			material_configs.append(config.stem)
	return material_configs


def get_material_config( material_type='metallic_roughness' ):
	material_config_path = Path( Path(__file__).parent.absolute(), 'materials', f'{material_type}.json')
	if material_config_path.is_file:
		with open(material_config_path) as json_file:    
			material_config = json.load(json_file)
	
		return material_config


def channel_pack_texture(texture_list, packing_dictionary, output_path, log_fn=None):
	def log( msg ):
		if log_fn:
			log_fn( msg )
		else:
			print(msg)

	log(f'Texture: Channel Packing {output_path.stem}...')
	for idx, texture in enumerate(texture_list):
		try:
			channel_image = Image.open(str(texture)).getchannel(idx)
		except ValueError: #its an alpha texture
			channel_image = Image.open(str(texture)).convert('L')			
		packing_dictionary[idx] = channel_image
	if len(packing_dictionary) < 4:
		image = Image.merge("RGB", packing_dictionary)
	else:
		image = Image.merge("RGBA", packing_dictionary)
	
	image.save(str(output_path)) #save the packed texture into the output directory


def channel_pack_textures( temp_dir, 
						   output_dir,
						   texture_dict, 
						   texture_resolution, 
						   asset_name,
						   material_type='metallic_roughness',
						   log_fn=None ):
	def log( msg ):
		if log_fn:
			log_fn( msg )
		else:
			print(msg)

	if not output_dir.exists():
		output_dir.mkdir(parents=True)
	image = Image.new("RGB", (texture_resolution, texture_resolution), ImageColor.getcolor("#000000", "RGB"))

	for key, value in texture_dict.items():
		if value.startswith('#'):
			image.paste( ImageColor.getcolor(value, "RGB"), [0,0,image.size[0],image.size[1]])			
			image.save(temp_dir / f'{asset_name}_{key}.png')
		else:
			pass
	
	#generate packing dict as a list of paths mapped to the channel
	packing_dictionary = get_material_config(material_type)["Packing"][0]
	for output, texture_list in packing_dictionary.items():
		for idx, texture in enumerate(texture_list):
			texture_suffix = packing_dictionary[output][idx]
			packing_dictionary[output][idx] = Path(temp_dir / f'{asset_name}_{texture_suffix}.png')
	
	#pack the textures
	packed_output_textures = dict()
	packed_output_textures['Textures'] = dict()
	channel_pack_threads = list()
	for output, texture_list in packing_dictionary.items():		
		output_path = Path(output_dir / f'{asset_name}_{output}.png')
		packed_output_textures['Textures'][output] = output_path
		thread = Thread(target = channel_pack_texture, args = (texture_list, packing_dictionary[output], output_path, log_fn))
		channel_pack_threads.append(thread)
	
	for thread in channel_pack_threads:
		thread.start()
		thread.join()

	return packed_output_textures