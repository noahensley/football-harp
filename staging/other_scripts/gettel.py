import bmp280

if __name__ == "__main__":
    
    ##################################################
    #                                                #                  
    # DIREWOLF COMMENTCMD                            #
    #                                                #
    ##################################################
    data_list = []

    delimiter = ","

    try:
        bmp280_data = bmp280.read_sensor()
        for data in bmp280_data:
            data_list.append(data)
    except Exception as e:
        print(f"Unable to read from bmp280: {e}")

    telemetry = delimiter.join(data_list)
    print(telemetry)
