from bigchaindb_driver import BigchainDB
import time

### BigchainDB Connection

bdb_root_url = 'http://localhost:9984'
bdb = BigchainDB(bdb_root_url)

### BigchainDB Keys

victor_priv = 'YOURPRIVATEKEYHERE'
victor_pub = 'YOURPUBLICKEYHERE'

### Raspberry Data

raspberry_asset = {
    'data': {
        'raspberry pi': {
            'serial_number': 'RPI01',
            'owner': 'UPM'
        },
    },
}

raspberry_asset_metadata = {
    'Environment Parameters': 'Here goes sensor data'
}

### Sending Data to BigchainDB
def send_to_bdb(sensor_data):

    raspberry_asset['data']['raspberry pi']['Storage TimeStamp'] = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    raspberry_asset_metadata = sensor_data

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=victor_pub,
        asset=raspberry_asset,
        metadata=raspberry_asset_metadata
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=victor_priv
    )

    print(fulfilled_creation_tx)

    bdb.transactions.send(fulfilled_creation_tx)
