while True:    
    live_status = input("Would you like to upload a video or livestream?(upload/stream)")
    if live_status in ["upload", "stream"]:
        break
    print("Please enter upload or stream")
    if live_status == "upload":
        path_to_video = input("Please enter the path to your video")
    elif live_status == "stream":
        if input("Would you like to save this video?(Enter y/n): ") == "y":
            # Where to save
            # Always save there?
            pass