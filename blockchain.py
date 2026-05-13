import hashlib, json, time, os

CHAIN_FILE = "chain_store.json"

class Blockchain:
    def __init__(self):
        self.chain = []
        if os.path.exists(CHAIN_FILE):
            try:
                with open(CHAIN_FILE, 'r') as f:
                    saved = json.load(f)
                    self.chain = saved.get("chain", [])
            except:
                self.create_block(1, '0', {"note": "genesis"})
        else:
            self.create_block(1, '0', {"note": "genesis"})

    def create_block(self, proof, previous_hash, data):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': data
        }
        self.chain.append(block)
        self.save_chain()
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_val = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] == "0000":
                return new_proof
            new_proof += 1

    def hash(self, block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr['previous_hash'] != self.hash(prev):
                return False
        return True

    def add_product(self, data):
        prev_block = self.get_previous_block()
        proof = self.proof_of_work(prev_block['proof'])
        prev_hash = self.hash(prev_block)
        return self.create_block(proof, prev_hash, data)

    def find_by_batch(self, batch):
        return [b for b in self.chain if b['data'].get('batch') == batch]

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump({'chain': self.chain}, f, indent=2)
