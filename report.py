
import tools.Reporting as Reporting
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.figure
from PIL import Image, ImageDraw, ImageFont

database_file = "transactions.sqlite"
bankdb = Reporting.Reporting(database_file)

start_date = "2023-01-01"
end_date = '2023-12-31'

kindle_screen = (600,800)

# ---------------------------------------------------------------
def scale(image, scalefactor):
    width = image.width
    height = image.height
    return image.resize((round(width*scalefactor), round(height*scalefactor)))

# ---------------------------------------------------------------
# https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil
def draw_text_90_into (text: str, into, at):
    # Measure the text area
    font = ImageFont.truetype ('Arial.ttf', 12)
    #wi, hi = font.getsize (text)
    _, _, wi, _ = font.getbbox(text)
    #hight based on all lower case (to allow for desenders)
    _, _, _, hi = font.getbbox('abcdefghijklmnopqrstuvwxyzs')

    # Copy the relevant area from the source image
    img = into.crop ((at[0], at[1], at[0] + hi, at[1] + wi))

    # Rotate it backwards
    img = img.rotate (90, expand = 1)

    # Print into the rotated area
    d = ImageDraw.Draw (img)
    d.text ((0, 0), text, font = font, fill = (255, 255, 255))

    # Rotate it forward again
    img = img.rotate (270, expand = 1)

    # Insert it back into the source image
    # Note that we don't need a mask
    into.paste (img, at)

# ---------------------------------------------------------------
def plot_personal_spending(imgfilename):

    data = bankdb.spending_by_tag(start_date, end_date, "bernadette")
    bspend = 0.0
    for row in data:
        bspend += row['amount']
    
    #print(bspend)
    # Circle 1
    # ['bernadette','nick']
    # ['amount',    'amount']

    # Circle 2
    # ['b-cat1', 'b-cat2', 'n-cat1']
    # ['amount1','amount2','amount3']

    data2 = bankdb.spending_by_tag(start_date, end_date, "nick")
    nspend = 0.0
    for row in data2:
        nspend += row['amount']

    amount = [abs(nspend), abs(bspend)]
    cat = [f'Nick (${abs(nspend):.2f})',f'Bernadette (${abs(bspend):.2f})']

    size = 0.3

    # https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html
    fig1, ax1 = plt.subplots()

    ax1.pie(amount,
            radius = 1,
            #labels=cat,
            #autopct='%1.1f%%',
            startangle=90,
            colors=['0.5','0.0'],
            wedgeprops=dict(width=size, edgecolor='w',linewidth=3)
            )

    # ax1.pie(amount2,
    #         radius = 1-size,
    #         labels=cat2,
    #         #autopct='%1.1f%%',
    #         startangle=90,
    #         wedgeprops=dict(width=size, edgecolor='w')
    #         )

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    kwargs = dict(size=20, fontweight='normal', va='center')
    ax1.text(0, 0, f'T:\${(abs(nspend)+abs(bspend)):.2f}\nN:\${abs(nspend):.2f}\nB:\${abs(bspend):.2f}', ha='center', **kwargs)
    ax1.set_title("Discretionary Spending")
    plt.savefig(imgfilename, bbox_inches='tight',format='png', transparent=True)
    #plt.savefig(imgfilename, bbox_inches='tight',format='png')
    #plt.show()
    

# ---------------------------------------------------------------
def plot_spend_vrs_income(imgfilename):

    income = bankdb.income(start_date, end_date)
    income_amount = income[0]['amount']

    spend = bankdb.spend(start_date, end_date)
    spend_amount = spend[0]['amount']

    amount = [abs(income_amount), abs(spend_amount)]
    # cat = [f'Nick (${abs(nspend):.2f})',f'Bernadette (${abs(bspend):.2f})']

    size = 0.3
    
    # https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html
    fig1, ax1 = plt.subplots()

    ax1.pie(amount,
            radius = 1,
            #labels=cat,
            #autopct='%1.1f%%',
            startangle=90,
            colors=['0.0','0.5'],
            wedgeprops=dict(width=size, edgecolor='w',linewidth=3)
            )

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    kwargs = dict(size=20, fontweight='normal', va='center')
    ax1.text(0, 0, f'N:\${income_amount+spend_amount:.2f}\nI:\${income_amount:.2f}\nS:-${abs(spend_amount):.2f}', ha='center', **kwargs)
    ax1.set_title("Spending vrs Income")
    plt.savefig(imgfilename, bbox_inches='tight',format='png', transparent=True)
    #plt.savefig(imgfilename, bbox_inches='tight',format='png')
    return fig1

# ---------------------------------------------------------------
def plot_spend_by_category(imgfilename):

    data2 = bankdb.spending_by_cat2(start_date, end_date, ignore_cat="transfer income work")
    cat = []
    amount = []
    cat2 = []
    amount2 = []
    for row in data2:
        if row['cat1'][:8] in cat:
            amount[cat.index(row['cat1'][:8])] += abs(row['amount'])
        else:
            cat.append(row['cat1'][:8])
            amount.append(abs(row['amount']))
        
        cat2.append(row['cat2'])
        amount2.append(abs(row['amount']))
        
    size = 0.08

    # https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html
    fig1, ax1 = plt.subplots()

    # Outer Ring - Cat2
    wedges, texts = ax1.pie(amount2,
            radius = 1,
            labels=cat2,
            rotatelabels =True,
            labeldistance=1.0,
            colors=['0.0'],
            #autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(width=4*size, edgecolor='w'),
            textprops = dict(va="center", rotation_mode = 'anchor')
            )

    # Inner Ring - Cat1
    wedges, texts = ax1.pie(amount,
            radius = 1-3*size,
            labels=cat,
            #autopct='%1.1f%%',
            rotatelabels=True,
            labeldistance=0.6,
            colors=['0.0'],
            startangle=90,
            wedgeprops=dict(width=size, edgecolor='w'),
            textprops = dict(ha="center", va="center", rotation_mode = 'anchor')
            )

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig(imgfilename, bbox_inches='tight',format='png', transparent=True)


def draw_spend_by_category(pilimage):
    '''Create a plot (not using matplotlib'''
    width = 25
    height = kindle_screen[1]

    # jebus this needs refactoring - what a hack just to avoid using numpy
    data2 = bankdb.spending_by_cat2(start_date, end_date, ignore_cat="transfer income work")
    cat = []
    amount = []
    amountcumsum = []
    cat2 = []
    amount2 = []
    amount2cumsum = []
    for row in data2:
        if row['cat1'] in cat:
            amount[cat.index(row['cat1'])] += abs(row['amount'])
        else:
            cat.append(row['cat1'])
            amount.append(abs(row['amount']))
        
        cat2.append(row['cat2'])
        amount2.append(abs(row['amount']))

    for i, item in enumerate(amount):
        if i == 0:
            amountcumsum.append(item)
        else:
            amountcumsum.append(amountcumsum[i-1]+item)

    for i, item in enumerate(amount2):
        if i == 0:
            amount2cumsum.append(item)
        else:
            amount2cumsum.append(amount2cumsum[i-1]+item)


    scale = height/sum(amount)

    draw = ImageDraw.Draw(pilimage)

    for i, rect in enumerate(cat):
        # [x0, y0, x1, y1]
        x0 = 0
        if i == 0:
            y0 = 0
        else:
            y0 = amountcumsum[i-1]*scale
        x1 = width
        y1 = y0 + amount[i]*scale
        draw.rectangle([x0, y0, x1, y1], fill='black', outline='white')

        #rotated text
        draw_text_90_into(rect, pilimage, (round(x0)+2,round(y0)+2))
    
    for i, rect in enumerate(cat2):
        # [x0, y0, x1, y1]
        x0 = width
        if i == 0:
            y0 = 0
        else:
            y0 = amount2cumsum[i-1]*scale
        x1 = width*2
        y1 = y0 + amount2[i]*scale
        draw.rectangle([x0, y0, x1, y1], fill='black', outline='white')

        #rotated text
        draw_text_90_into(rect, pilimage, (round(x0)+2,round(y0)+2))
# ---------------------------------------------------------------
def main():
    print(f"Report Range: {start_date} to {end_date}")
    income = bankdb.income(start_date, end_date)
    income_amount = income[0]['amount']
    print(f"Income: {income_amount}")
    spend = bankdb.spend(start_date, end_date)
    spend_amount = spend[0]['amount']
    print(f"Spend: {spend_amount}")
    print(f"Net: {income_amount + spend_amount}")

    # discretionary spending
    nick = bankdb.spending_by_tag(start_date, end_date, "nick")
    nick_amount = 0.0
    for row in nick:
        nick_amount += row['amount']
    bernadette = bankdb.spending_by_tag(start_date, end_date, "bernadette")
    bernadette_amount = 0.0
    for row in bernadette:
        bernadette_amount += row['amount']
    print(f"Nick: {nick_amount}")
    print(f"Bernadette: {bernadette_amount}")

    test = bankdb.spending_by_tag(start_date, end_date, "nick bernadette")
    print(tabulate(test))

    plot_personal_spending('temp/personalspend.png')
    plot_spend_vrs_income("temp/spendvrsincome.png")
    #plot_spend_by_category("temp/spendbycat.png")
    
    # Build the Kindle Image
    kindle = Image.new('RGBA', kindle_screen, (255,255,255,255))
    # Open and resize
    personalspend = Image.open('temp/personalspend.png')
    personalspend = scale(personalspend, 0.6)
    spendincome = Image.open('temp/spendvrsincome.png')
    spendincome = scale(spendincome, 0.6)
    #spendcat = Image.open("temp/spendbycat.png")
    #image1 = image1.resize((426, 240))
    kindle.paste(personalspend,(0,0),mask=personalspend)
    kindle.paste(spendincome,(300,0),mask=spendincome)
    #kindle.paste(spendcat,(300-round(spendcat.width/2),180),mask=spendcat)
    draw_spend_by_category(kindle)
    kindle.save("temp/report.png","PNG")
    kindle.show()

# -------------------------------------------
if __name__ == '__main__':
    main()