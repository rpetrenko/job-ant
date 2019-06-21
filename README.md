### Installation instruction for macOS
* install requirements
```bash
pip install -r requirements.txt
```

* install openCV binaries (this might take some time)
```bash
brew install opencv
```

* link python package in venv
```bash
cd job-ant/venv/lib/python3.6/site-packages
ln -s "/usr/local/opt/opencv@4/lib//python3.7/site-packages/cv2/python-3.7/cv2.cpython-37m-darwin.so" cv2.so
```