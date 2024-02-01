def analyze_price_channel(output):
    text = ""

    # [5] status        [11] prct special value (min/max etc)
    if output[5] == "low":
        if float(output[3]) / float(output[11]) > float(1.10):
            # Cena ponad 10% od dołka (pod kanalem cenonwym)
            text = "BUY"

        else:
            if int(output[9] > int(10)):
                # Cena jest blisko dołka przez ponad 10 dni (pod kanalem cenonwym)

                text = "BUY1"
            else:
                # Cena spadla pod kanal cenonwy
                # if spread in channel price > 10%
                if float(output[17]) / float(output[15]) >= 1.10:
                    text = "BUY3"
                else:
                    text = "BUY2"
        # print(output)
        output.append(text)
        # print(output)
    if output[5] == "in":
        if output[7] == "low":
            if float(output[13]) < float(1):
                # Cena wskoczyła w kanał z dołka
                # print("Rised above the bottom line - last moment for buying")
                text = "Late Buying"
            else:
                # Cena jest ponad średnią, ale w kanale - dom. rośnie bo wyszła z dołka
                # print("Stable and going up - should be expensive soon")
                text = "Close to Sell"
        if output[7] == "upper":
            if float(output[13]) < float(1):
                # Cena jest w kanale - ale spada poniżej średniej - dom. była wczesniej nad kanałek
                # print("Going down - should be cheap soon")
                text = "Close to Buy"
            else:
                # Cena spadła do kanału z gorki

                # print("Starting to decline - last moment for selling")
                text = "Late Selling"
        else:
            text = "No change"
        output.append(text)
    if (output[5] == "upper") and (float(output[3]) > float(output[18])):
        if float(output[3]) / float(output[11]) > float(0.9):
            # Cena buduje szczyt - jestes w topie lub w 10% odleglosci od niego
            text = "SELL"
        else:
            if int(output[9] > int(10)):
                # cena zrobila szczyt i utrzymuje wartosc wieksza niz 10% od szczytu ale wciaz jest droga
                text = "SELL1"
            else:
                # cena spadla o wiecej niz 10% od szczytu w ostatnich dniach( <10 ergo. szybko),ale wciaz jest droga
                # if spread in channel price > 10%
                if float(output[17]) / float(output[15]) >= 1.10:
                    text = "SELL3"
                else:
                    text = "SELL2"
        output.append(text)
    elif (output[5] == "upper") and (float(output[3]) <= float(output[18])):
        # Cena odbija ale jest ryzyko ze sell w stosunku do buya bedzie na -
        # text = "Starting to rise - risky Buy"
        text = "Selling not adviced - possible High Buying Price"
        output.append(text)
    # print("")
    return