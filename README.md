> [!WARNING]  
> This project is intended strictly for educational and research purposes only.  
> The author assumes no responsibility for any consequences arising from the use of this tool, including but not limited to account bans or data loss.  
> The author is not responsible for any bans from the use of this tool!  
> Use it at your own risk.
> Follow the [SYBO TOS](https://sybogames.com/terms-of-service) or whatever

# SubwaySurfers API

You can interact with the internal api that is used by the SubwaySurfers game app.

---

## Requirements

- `grpcio` and `protobuf` Python packages installed
- Protocol Buffers Compiler (`protoc`) installed and accessible via command line

## Setup and Usage

```bash
pip install -r requirements.txt
cd send
protoc --python_out=. player.proto
```

```bash
python sendrpc.py
python sendjson.py
```
