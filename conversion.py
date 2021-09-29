def weigh(unit,value):
    if unit =='kg':
        mass= round(float(value)*2.204,2)
        return f"{value}kg is equal to {mass}lb."
    if unit =='lb':
        mass= round(float(value*0.453592),2)
        return f"{value}lb is equal to {mass}kg."
   
def bodymass(weight,height):
    try:
        z=round(float(weight)/(float(height/100)*float(height/100)),2)
        if z<18.5:
            return f"Your body mass is {z}, and according to this index you are considered as underweighted"
        elif z>18.5 and z<29.9:
            return f"Your body mass is {z}, and according to this index you have normal weight"
        elif 30<z<34.9:
            return f"Your body mass is {z}, and according to this index you have Obesity class 1"
        elif 35<z<39.9:
            return f"Your body mass is {z}, and according to this index you have Obesity class 2"
        elif z>40:
            return f"Your body mass is {z}, and according to this index you have Obesity class 3"
        else:
            return "The value you have entered is not correct"
    except NameError:
        print('The value should be either integer or float')
        
def fahrenheit(t,celisius):
    if t== 'c': # Convert Celisius to Fahrenheit
        x= round(float(celisius*9/5)+32,2)
    elif t== 'f':
        x= round(float(celisius-32)*5/9,2)
    else:
        return "The acceptable units are Celisious or Fahrenheit"
    return f"The tempurature is {x} F degrees."
    



print (weigh('lb',76))

print(bodymass(56,1.16))