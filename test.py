import asyncio

def stop_all_event_loops():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.stop()  # Dừng loop
            loop.close()  # Đóng loop hoàn toàn
            print("Event loop đã bị dừng và đóng.")
    except RuntimeError:
        print("Không có event loop nào đang chạy.")

stop_all_event_loops()
