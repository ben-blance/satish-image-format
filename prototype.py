#!/usr/bin/env python3
"""
SATISH Image Format Prototype
A custom image format that stores pixel data as hex color values
"""

import struct
from PIL import Image
import os

class SatishImage:
    def __init__(self):
        self.magic = b"SATI"
        self.version = 1
        
    def rgb_to_hex(self, r, g, b):
        """Convert RGB values to hex string"""
        return f"{r:02x}{g:02x}{b:02x}"
    
    def hex_to_rgb(self, hex_color):
        """Convert hex string to RGB tuple"""
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def save_satish(self, image_path, output_path):
        """Convert a regular image to .satish format"""
        try:
            # Open and convert image to RGB
            img = Image.open(image_path).convert('RGB')
            width, height = img.size
            
            # Get pixel data
            pixels = list(img.getdata())
            
            # Convert RGB pixels to hex strings
            hex_pixels = []
            for r, g, b in pixels:
                hex_pixels.append(self.rgb_to_hex(r, g, b))
            
            # Write to .satish file
            with open(output_path, 'wb') as f:
                # Header
                f.write(self.magic)                    # 4 bytes: "SATI"
                f.write(struct.pack('>H', width))      # 2 bytes: width
                f.write(struct.pack('>H', height))     # 2 bytes: height
                f.write(struct.pack('B', 3))           # 1 byte: channels (RGB=3)
                f.write(struct.pack('B', self.version)) # 1 byte: version
                
                # Pixel data as hex strings (6 chars per pixel)
                pixel_data = ''.join(hex_pixels)
                f.write(pixel_data.encode('ascii'))
            
            print(f"✅ Saved {output_path}")
            print(f"   Original: {image_path}")
            print(f"   Size: {width}x{height}")
            print(f"   Pixels: {len(hex_pixels)}")
            
        except Exception as e:
            print(f"❌ Error saving: {e}")
    
    def load_satish(self, satish_path):
        """Load a .satish file and return image data"""
        try:
            with open(satish_path, 'rb') as f:
                # Read header
                magic = f.read(4)
                if magic != self.magic:
                    raise ValueError(f"Invalid file format. Expected {self.magic}, got {magic}")
                
                width = struct.unpack('>H', f.read(2))[0]
                height = struct.unpack('>H', f.read(2))[0] 
                channels = struct.unpack('B', f.read(1))[0]
                version = struct.unpack('B', f.read(1))[0]
                
                # Read pixel data
                pixel_data = f.read().decode('ascii')
                
                # Convert hex strings back to RGB
                pixels = []
                for i in range(0, len(pixel_data), 6):
                    hex_color = pixel_data[i:i+6]
                    if len(hex_color) == 6:
                        pixels.append(self.hex_to_rgb(hex_color))
                
                return {
                    'width': width,
                    'height': height,
                    'channels': channels,
                    'version': version,
                    'pixels': pixels
                }
                
        except Exception as e:
            print(f"❌ Error loading: {e}")
            return None
    
    def satish_to_image(self, satish_path, output_path):
        """Convert .satish back to a regular image format"""
        data = self.load_satish(satish_path)
        if not data:
            return
        
        try:
            # Create PIL image
            img = Image.new('RGB', (data['width'], data['height']))
            img.putdata(data['pixels'])
            
            # Save as regular image
            img.save(output_path)
            print(f"✅ Converted {satish_path} → {output_path}")
            
        except Exception as e:
            print(f"❌ Error converting: {e}")
    
    def view_satish(self, satish_path):
        """Display a .satish image"""
        data = self.load_satish(satish_path)
        if not data:
            return
        
        try:
            img = Image.new('RGB', (data['width'], data['height']))
            img.putdata(data['pixels'])
            img.show()
            
            print(f"📷 Viewing: {satish_path}")
            print(f"   Size: {data['width']}x{data['height']}")
            print(f"   Channels: {data['channels']}")
            print(f"   Version: {data['version']}")
            
        except Exception as e:
            print(f"❌ Error viewing: {e}")
    
    def inspect_satish(self, satish_path):
        """Show detailed info about a .satish file"""
        data = self.load_satish(satish_path)
        if not data:
            return
        
        print(f"🔍 SATISH File Inspection: {satish_path}")
        print(f"   Format: SATISH v{data['version']}")
        print(f"   Dimensions: {data['width']} x {data['height']}")
        print(f"   Channels: {data['channels']}")
        print(f"   Total Pixels: {len(data['pixels'])}")
        
        # Show first few pixels as hex
        print(f"   First 5 pixels (hex):")
        for i, (r, g, b) in enumerate(data['pixels'][:5]):
            hex_color = self.rgb_to_hex(r, g, b)
            print(f"     Pixel {i+1}: #{hex_color} (RGB: {r},{g},{b})")

def main():
    """Demo the SATISH format"""
    satish = SatishImage()
    
    print("🎨 SATISH Image Format Prototype")
    print("=" * 40)
    
    # Example usage
    print("\n📝 Usage Examples:")
    print("satish.save_satish('input.jpg', 'output.satish')")
    print("satish.view_satish('image.satish')")
    print("satish.satish_to_image('image.satish', 'converted.png')")
    print("satish.inspect_satish('image.satish')")
    
    # Interactive mode
    while True:
        print("\n" + "="*40)
        print("Choose an action:")
        print("1. Convert image to .satish")
        print("2. View .satish image") 
        print("3. Convert .satish to image")
        print("4. Inspect .satish file")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            input_path = input("Enter input image path: ").strip()
            output_path = input("Enter output .satish path: ").strip()
            if not output_path.endswith('.satish'):
                output_path += '.satish'
            satish.save_satish(input_path, output_path)
            
        elif choice == '2':
            satish_path = input("Enter .satish file path: ").strip()
            satish.view_satish(satish_path)
            
        elif choice == '3':
            satish_path = input("Enter .satish file path: ").strip()
            output_path = input("Enter output image path: ").strip()
            satish.satish_to_image(satish_path, output_path)
            
        elif choice == '4':
            satish_path = input("Enter .satish file path: ").strip()
            satish.inspect_satish(satish_path)
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()