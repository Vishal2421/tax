from flask import Flask, render_template, request
import pandas as pd
import num2words


app = Flask(__name__)

# Your function that takes an integer and returns a DataFrame
def tax_new(sal):
    new_tax_slab_rate=[5,10,15,20,25,30]
    new_tax_slab=[400000,800000,1200000,1600000,2000000,2400000]
    salary=sal
    if salary<=1200000:
        tax_pay=0
        slab_1=0
        slab_2=0
        slab_3=0
        slab_4=0
        slab_5=0
        slab_6=0
        print('wohho no tax in new tax')
    else:
        slab_1=(new_tax_slab[1]-new_tax_slab[0])*new_tax_slab_rate[0]/100  ## for 4 to 8 lakh
        slab_2=(new_tax_slab[2]-new_tax_slab[1])*new_tax_slab_rate[1]/100   ## for 8 to 12 lakhs
    
        # for 12 to 16 lakh
        if salary>new_tax_slab[2]:
            if salary>new_tax_slab[2] and salary<=new_tax_slab[3]:
                slab_3=(salary-new_tax_slab[2])*new_tax_slab_rate[2]/100
            else :
                slab_3=(new_tax_slab[3]-new_tax_slab[2])*new_tax_slab_rate[2]/100
        else:
            slab_3=0
        # for 16 to 20 lakh
        if salary>new_tax_slab[3]:
            if salary>new_tax_slab[3] and salary<=new_tax_slab[4]:
                slab_4=(salary-new_tax_slab[3])*new_tax_slab_rate[3]/100
            else :
                slab_4=(new_tax_slab[4]-new_tax_slab[3])*new_tax_slab_rate[3]/100
        else:
            slab_4=0
        # for 20 to 24 lakh
        if salary>new_tax_slab[4]:
            if salary>new_tax_slab[4] and salary<=new_tax_slab[5]:
                slab_5=(salary-new_tax_slab[4])*new_tax_slab_rate[4]/100
            else :
                slab_5=(new_tax_slab[5]-new_tax_slab[4])*new_tax_slab_rate[4]/100
        else:
            slab_5=0
        # for above 24 lakh
        if salary>new_tax_slab[5]:
            slab_6=(salary-new_tax_slab[5])*new_tax_slab_rate[5]/100
        else:
            slab_6=0
        tax_pay=slab_1+slab_2+slab_3+slab_4+slab_5+slab_6

    return [tax_pay,slab_1,slab_2,slab_3,slab_4,slab_5,slab_6]

def tax_old(sal):
    old_tax_slab_rate=[5,10,15,20,30]
    old_tax_slab=[300000,700000,1000000,1200000,1500000]
    salary=sal
    if salary<=700000:
        tax_pay=0
        slab_1=0
        slab_2=0
        slab_3=0
        slab_4=0
        slab_5=0
        print('wohho no tax in old')
    else:
        slab_1=(old_tax_slab[1]-old_tax_slab[0])*old_tax_slab_rate[0]/100  ## for 3 to 7 lakh
    
        # for 7 to 10 lakh
        if salary>old_tax_slab[1]:
            if salary>old_tax_slab[1] and salary<=old_tax_slab[2]:
                slab_2=(salary-old_tax_slab[1])*old_tax_slab_rate[1]/100
            else :
                slab_2=(old_tax_slab[2]-old_tax_slab[1])*old_tax_slab_rate[1]/100
        else:
            slab_2=0

        
        # for 10 to 12 lakh
        if salary>old_tax_slab[2]:
            if salary>old_tax_slab[2] and salary<=old_tax_slab[3]:
                slab_3=(salary-old_tax_slab[2])*old_tax_slab_rate[2]/100
            else :
                slab_3=(old_tax_slab[3]-old_tax_slab[2])*old_tax_slab_rate[2]/100
        else:
            slab_3=0
        # for 12 to 15 lakh
        if salary>old_tax_slab[3]:
            if salary>old_tax_slab[3] and salary<=old_tax_slab[4]:
                slab_4=(salary-old_tax_slab[3])*old_tax_slab_rate[3]/100
            else :
                slab_4=(old_tax_slab[4]-old_tax_slab[3])*old_tax_slab_rate[3]/100
        else:
            slab_4=0
        # for above 15 lakh
        if salary>old_tax_slab[4]:
            slab_5=(salary-old_tax_slab[4])*old_tax_slab_rate[4]/100
        else:
            slab_5=0
        tax_pay=slab_1+slab_2+slab_3+slab_4+slab_5
    
    return [tax_pay,slab_1,slab_2,slab_3,slab_4,slab_5]

def tax_com(sal):
    sal=sal-75000
    old=tax_old(sal)
    new=tax_new(sal)
    A_old=sal+75000
    T_old=old[0]
    final_old=(A_old*(1-(0.5*0.25) + (0.1*0.3))/1.1 -T_old)/12
    A_new=sal+75000
    T_new=new[0]
    final_new=(A_new*(1-(0.5*0.25) + (0.1*0.3))/1.1 -T_new)/12

    old_dic={'Tax_algo' :['Old'],'Total Tax' :[old[0]] , 'Slab_1' : [old[1]], 'Slab_2' : [old[2]], 'Slab_3' : [old[3]], 'Slab_4' : [old[4]], 'Slab_5' : [old[5]]}
    old_df=pd.DataFrame(old_dic)
    old_df['Monthly in hand']=final_old
    new_dic={'Tax_algo' :['New'],'Total Tax' :[new[0]] , 'Slab_1' : [new[1]], 'Slab_2' : [new[2]], 'Slab_3' : [new[3]], 'Slab_4' : [new[4]], 'Slab_5' : [new[5]], 'Slab_6' : [new[6]]}
    new_df=pd.DataFrame(new_dic)
    new_df['Monthly in hand']=final_new
    print(f'profit of {old[0]-new[0]} i.e {num2words.num2words(old[0]-new[0], lang='en_IN')} rupees')
    df=pd.concat([new_df,old_df])
    return df.set_index('Tax_algo')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the integer from the form
        value = float(request.form['value'])
        # Generate the DataFrame
        df = tax_com(value)
        # Convert the DataFrame to HTML for rendering
        df_html = df.to_html(classes='table table-striped')
        return render_template('index.html', table=df_html)
    return render_template('index.html', table=None)

if __name__ == '__main__':
    app.run(debug=True)
