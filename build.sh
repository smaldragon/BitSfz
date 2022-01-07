echo "0- Deleting previous version"
rm -r dist/
echo "1- Running pyinstaller"
pyinstaller --onefile main.py --name bitSFZ
echo "2- Building wave library"
cc -fPIC -shared -o dist/libWave.so wave_gen.c
echo "3- Copying assets"
cp -R assets dist/assets
echo "4- Making Instruments Folder"
mkdir dist/instruments