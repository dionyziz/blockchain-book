# Overview

For this course, we will develop our own blockchain. Each student will write their own
independent implementation of a node for our network in their programming language of
choice. This document outlines how the system will work and how nodes will communicate.

During your implementation, be aware that neighbouring nodes can be malicious. Your
implementation must be resilient to simple and complex attacks. Simple attacks can be
the supply of invalid data. Complex attacks can involve signatures, proof-of-work,
double spending, and blocks, all of which must be validated carefully.

The chain is a variable-difficulty proof-of-work UTXO-based blockchain over a TCP
network protocol.

## Networking

The peer-to-peer network works over TCP. We use TCP port 18018. Your node must listen
to this port and connect to peers using this port. If your node is running behind NAT,
make sure this port is forwarded.

## Bootstrapping

Your node will initially connect to a list of known peers. From there, it will build
its own list of known peers. We will maintain a list of bootstrapping peer IPs / domains
in this document when they become available.

## Data validation

Your client must disconnect from their peer in case they receive invalid data. Be rigorous
about network data validation and do not accept malformed data. Log any incorrect data received
to help us with debugging.

# Cryptographic Primitives

## Hashes

We use SHA-256 as our hash for everything. This is used both for content-addressible application
objects as well as proof-of-work. When hashes appear in our JSON, they should be in hexadecimal
format.

## Signatures

We use ECDSA signatures using SHA-256 hash as digest and the secp256k1 curve. Public keys consist
of a point `(x, y)` and should be byte-encoded in the
[uncompressed SEC format](https://www.oreilly.com/library/view/programming-bitcoin/9781492031482/ch04.html).
Signatures consist of a pair `(r, s)` and should be byte-encoded in the
[DER format](https://www.oreilly.com/library/view/programming-bitcoin/9781492031482/ch04.html).
Once a signature or public key is byte-encoded, it is converted to hex to represent as a string
within our JSON.
Whenever we refer to a "public key" or a "signature" in this protocol, we mean uncompressed SEC
or DER format byte-encoded hexified data respectively.

## Hexification

Hex strings must be in lower case.

# Application Objects

Application Objects are objects that must be stored by each node. These are content-addressed by
the SHA256 hash of their JSON representation. It is therefore important to have the same JSON
representation as other clients so that the same objects are addressed by the same hash. You
should normalize your JSON and ensure it is in
[canonical JSON form](https://github.com/cyberphone/json-canonicalization).
The examples in this document contain extra whitespace for readability, but these should not
be sent over the network.
The SHA256 of the JSON contents is the objectid.

An Application Object is a JSON dictionary containing the "type" key and further keys depending on its type.

There are two types of Application Objects: Transactions and Blocks. Their objectids are called txid
and blockid respectively.

## Transactions

This represents a transaction and has the type `transaction`. It contains the key `inputs` containing
an array of inputs, and the key `outputs` containing an array of outputs.

An input contains a pointer to a
previous output (the outpoint), and a signature. An input is a dictionary containing two
keys: An `outpoint` key and a `sig` key. The `outpoint` key contains a dictionary of two keys:
`txid` and `index`. The `txid` is the txid of a previous transaction, while the `index` is the natural
number (zero-based) indexing an output within that transaction. The `sig` key contains the (DER encoded)
signature.

Signatures are created using the private keys corresponding to the public keys that are pointed to
by their respective outpoint. Signatures are created on the plaintext which consists of the transaction
they (not their public keys!) are contained within, except that the `sig` values are all replaced with `null`.
This is necessary because a signature cannot sign itself.

An output is a dictionary with keys `value` and `pubkey`. The `value` is a non-negative integer indicating
how much value is carried by the output. The `pubkey` is a (uncompressed SEC encoded) public key, the
receipient of the money.

```json
{
  "type": "transaction",
  "inputs": [
    {
      "outpoint": {
        "txid": "f71408bf847d7dd15824574a7cd4afdfaaa2866286910675cd3fc371507aa196",
        "index": 0
      },
      "sig": "30450220397116930C282D1FCB71166A2D06728120CF2EE5CF6CCD4E2D822E8E0AE24A300221009E997D4718A7603942834FBDD22A4B856FC4083704EDE62033CF1A77CB9822A9"
    }
  ],
  "outputs": [
    {
      "pubkey": "0420f34c2786b4bae593e22596631b025f3ff46e200fc1d4b52ef49bbdc2ed00b26c584b7e32523fb01be2294a1f8a5eb0cf71a203cc034ced46ea92a8df16c6e9",
      "value": 5100000000
    }
  ]
}
```

If the transaction is a coinbase transaction, then it will not contain an `inputs` key.

## Blocks

This represents a block and has the type "block". It contains the key `txids`, which is a list of the txids within
the block, a `nonce` which is a 32-byte hexified value, a `previd` which is the blockid of the previous block in
the chain, a `created` which is an (integer) UNIX timestamp in seconds, and a `T` which is a 32-byte hexadecimal integer
and is the mining target. Optionally it can contain a `miner` field, which can be any ASCII-printable string up to 32
characters long.

```json
{
  "type": "block",
  "txids": [
    "740bcfb434c89abe57bb2bc80290cd5495e87ebf8cd0dadb076bc50453590104"
  ],
  "nonce": "a26d92800cf58e88a5ecf37156c031a4147c2128beeaf1cca2785c93242a4c8b",
  "previd": "0024839ec9632d382486ba7aac7e0bda3b4bda1d4bd79be9ae78e7e1e813ddd8",
  "created": "1622825642",
  "T": "003a000000000000000000000000000000000000000000000000000000000000",
  "miner": "dionyziz"
}
```

Block validity mandates that the block satisfies the proof-of-work equation:
`blockid < T`.

The genesis block has a null `previd`. This is our genesis block:

```json
{
  "type": "block",
  "txids": [],
  "nonce": "ea20f18102256b6af34a9ff33291216ba6c28486a01620e6a907eb67531685c8",
  "previd": null,
  "created": "1622826460",
  "T": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
  "miner": "dionyziz"
}
```

All valid chains must extend genesis. Each block must have a timestamp which is later than its
predecessor.

The `nonce` value for this block is the SHA256 hash of the following (linebreak terminated) string:

"The Guardian Science 4 Jun 2021: SpaceX rocket heads to ISS with squid, toothpaste and avocados"

The `txids` in a block may contain one coinbase transaction. This transaction must be the first in the
txids. That transaction has no inputs. It has exactly one output which generates 50 * 10^9 new coins.

# Messages

Every message exchanged by two peers over TCP is a JSON message. These JSON messages are separated
from one another using '\n'. The JSON messages themselves must not contain new line endings
('\n'), but they may contain escaped line endings within their strings.

Every JSON message is a dictionary. This dictionary always has at least the key "type" set,
which is a string and defines the message types. Each message may contain its own keys depending
on its type.

## Hello

When you connect to another client, you must both send a { "type": "hello" } message. The message
must also contain a "version" key, which is always set to "0.1.0". If the version you receive differs
from "0.1" you must disconnect. You must exchange a hello message both ways before you exchange any
other message. If a message is sent prior to the hello message, you must close the connection.
Messages can be sent in any order after that.

```json
{
  "type": "hello",
  "version": "0.1.0"
}
```

## GetPeers

If you want to know what peers are known to your peer, you send them a `getpeers` message. This
message has no payload and must be responded-to with a `peers` message.

```json
{ "type": "getpeers" }
```

## Peers

This message can be volunteered or sent in response to a `getpeers` message. It contains a `peers`
key which is an array of peers. Every peer is a dictionary which contains one or more of:

- An `ipv4` key containing the IPv4 address of the peer
- An `ipv6` key containing the IPv6 address of the peer
- A `dns` key containing the domain name of the peer

Optionally, it can contain a a `port` key with the TCP port of the peer. Otherwise, this defaults
to 18018. It is up to your node implementation to decide which peers to share with your peers.

```json
{
  "type": "peers",
  "peers": [
    {
      "dns": "dionyziz.com",
      "ipv4": "139.162.130.195",
      "port": 18018
    },
    {
      "ipv4": "138.197.191.170"
    },
    {
      "ipv6": "fe80::f03c:91ff:fe2c:5a79"
    }
  ]
}
```

## GetObject

This message requests an object addressed by the given hash. It contains an `objectid` key which is the
address of the object.

```json
{
  "type": "getobject",
  "objectid": "0024839ec9632d382486ba7aac7e0bda3b4bda1d4bd79be9ae78e7e1e813ddd8"
}
```

## IHaveObject

This message advertises that the sending peer has an object with a given hash addressed by the `objectid` key.
The receiving peer may request the object (using `getobject`) in case it does not have it.

```json
{
  "type": "ihaveobject",
  "objectid": "0024839ec9632d382486ba7aac7e0bda3b4bda1d4bd79be9ae78e7e1e813ddd8"
}
```

In our gossiping protocol, whenever a peer receives a new object and validates it, it advertises the new object
to its peers.

## Object

This message sends an object from one peer to another. This can be voluntary, or as a response to a `getobject`
message. It contains an `object` key which contains the object in question.

```json
{
  "type": "object",
  "object": {
    "type": "block",
    "txids": [
      "740bcfb434c89abe57bb2bc80290cd5495e87ebf8cd0dadb076bc50453590104"
    ],
    "nonce": "a26d92800cf58e88a5ecf37156c031a4147c2128beeaf1cca2785c93242a4c8b",
    "previd": "0024839ec9632d382486ba7aac7e0bda3b4bda1d4bd79be9ae78e7e1e813ddd8",
    "created": "1622825642",
    "T": "003a000000000000000000000000000000000000000000000000000000000000"
  }
}
```

## GetMempool

Request the mempool of the peer with a message of type `getmempool`. There is no payload in this message.
The peer responds with a `mempool` message.

```json
{
  "type": "getmempool"
}
```

## Mempool

This message, with type `mempool`, is sent as a response to a `getmempool` message, or it can be volunteered.
It includes a list of all txids that the sending peer has in its mempool, i.e., are not
yet confirmed. These are included in an array with the key `txids`.

```json
{
  "type": "mempool",
  "txids": []
}
```

## GetChainTip

Request the current blockchain tip of the peer with a message of type `getchaintip`. There is no payload in this message.

```json
{
  "type": "getchaintip"
}
```

## ChainTip

This message, with type `chaintip`, is sent as a response to the `getchaintip` message, or it can be volunteer.
It includes a single key called `blockid` with the blockid of the current tip.

```json
{
  "type": "chaintip",
  "blockid": "0024839ec9632d382486ba7aac7e0bda3b4bda1d4bd79be9ae78e7e1e813ddd8"
}
```

The receiving peer can then use `getobject` to retrieve the block contents and then follow up with more
`getobject` messages for each `previd` recursively to retrieve the whole blockchain as needed.
