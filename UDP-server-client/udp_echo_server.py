import asyncio


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print("Received %r from %s" % (message, addr))
        print("Send: %r" % message)
        self.transport.sendto(data, addr)


async def main():
    print("Starting the UDP server...")

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(), local_addr=("127.0.0.1", 9999)
    )

    try:
        await asyncio.sleep(60)  # Serve for 1 minute.
    finally:
        transport.close()


asyncio.run(main())
