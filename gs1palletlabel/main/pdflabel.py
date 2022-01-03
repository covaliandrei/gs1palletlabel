import os
import treepoem
from fpdf import FPDF


def PdfLabel(order_number,
               supplier_name,
               destination_name,
               product_name,
               product_scu,
               boxes_per_pallet,
               weight_brutto,
               weight_netto,
               pallets_count):

    def gencode128(textdata):
        return treepoem.generate_barcode(
            barcode_type='code128',
            data=textdata,
            options={
                'width': '4',
                'height': '1',
            },
        )

    stringsz = [
            "GS1 LOGISTIC LABEL",
            "NUMARUL COMENZII",
            "FROM: ",
            "TO: ",
            "SORTIMENT",
            "CODUL SSCC",
            "NUMARUL DE CARTOANE DE PE PALET: ",
            "CANTITATEA BRUTA DE PE PALET: ",
            "CANTITATEA NETA DE PE PALET: ",
            "SSCC:"
        ]

        datas = [
            "",
            order_number,
            supplier_name,
            destination_name,
            product_name,
            product_scu,
            boxes_per_pallet,
            weight_brutto,
            weight_netto,
            "(00)"+product_scu
        ]

        if not os.path.exists('images\\' + datas[8] + '.png'):
            image = gencode128(datas[8])
            image.convert('1').save('images\\' + datas[8] + '.png')
        if not os.path.exists('images\\' + datas[9] + '.png'):
            image = gencode128(datas[9])
            image.convert('1').save('images\\' + datas[9] + '.png')

        pdf = FPDF('P', 'mm', 'A4')
        j = 1
        while j <= pallets_count:
            pdf.add_page("L")
            pdf.set_auto_page_break(True, 10)
            pdf.set_font("Arial", '', 10)
            pdf.set_top_margin(2)
            pdf.set_left_margin(2)
            pdf.set_right_margin(2)
            offset = 3
            i = 1
            while i <= 2:
                pdf.set_font('', '', 10)
                pdf.rect(offset + 3, 4, 141, 11)
                pdf.set_xy(offset + 3, 6)
                pdf.cell(0, 4, stringsz[0], 0, 1, "L", False)

                pdf.set_xy(offset + 23, 7)

                pdf.cell(0, 6, datas[0], 0, 1, "L", False)

                pdf.rect(offset + 3, 15, 141, 14)

                pdf.set_xy(offset + 3, 16)
                pdf.set_font('', '', 10)
                pdf.cell(0, 4, stringsz[2], 0, 1, "L", False)

                pdf.set_xy(offset + 30, 21)
                pdf.set_font('', 'B', 12)
                pdf.cell(0, 6, datas[2], 0, 1, "L", False)

                pdf.rect(offset + 3, 29, 141, 10)

                pdf.set_xy(offset + 3, 30)
                pdf.set_font('', '', 10)
                pdf.cell(0, 4, stringsz[3], 0, 1, "L", False)

                pdf.set_xy(offset + 30, 30)
                pdf.set_font('', 'B', 12)
                pdf.cell(0, 6, datas[3], 0, 1, "L", False)

                pdf.rect(offset + 3, 39, 141, 30)

                pdf.set_xy(offset + 28, 62)
                pdf.image('images\\' + datas[8] + '.png', offset + 8, 42, 60, 20)
                pdf.cell(0, 6, datas[8], 0, 1, "L", False)

                pdf.rect(offset + 3, 69, 141, 60)
                pdf.set_xy(offset + 30, 71)
                pdf.set_font('', 'B', 12)
                pdf.cell(0, 6, 'PALET NR. ' + str(j), 0, 1, "L", False)
                pdf.set_xy(offset + 3, 76)
                pdf.set_font('', '', 10)
                pdf.cell(0, 4, stringsz[1] + ' :  ' + datas[1], 0, 1, "L", False)
                pdf.set_xy(offset + 3, 82)
                pdf.cell(0, 4, stringsz[4] + ' :  ' + datas[4], 0, 1, "L", False)
                pdf.set_xy(offset + 3, 88)
                pdf.cell(0, 4, stringsz[5] + ' :  ' + datas[5], 0, 1, "L", False)

                pdf.set_xy(offset + 3, 94)
                pdf.cell(0, 4, stringsz[6] + ' :  ' + datas[6], 0, 1, "L", False)

                pdf.set_xy(offset + 3, 100)
                pdf.cell(0, 4, stringsz[7] + ' :  ' + datas[7], 0, 1, "L", False)

                pdf.set_xy(offset + 3, 106)
                pdf.cell(0, 4, stringsz[8] + ' :  ' + datas[8], 0, 1, "L", False)

                pdf.rect(offset + 3, 129, 141, 46)
                pdf.set_xy(offset + 8, 132)
                pdf.set_font('', 'B', 12)
                pdf.cell(0, 4, 'SSCC :  ' + datas[5], 0, 1, "L", False)
                pdf.image('images\\' + datas[9] + '.png', offset + 8, 138, 130, 26)
                pdf.set_xy(offset + 38, 166)
                pdf.set_font('', 'B', 18)
                pdf.cell(0, 4, datas[9], 0, 1, "L", False)
                offset = 146
                i += 1
            j += 1

        pdf.output('labels\\'+'order_number'+'.pdf', 'F')
        return 'labels\\' + 'order_number' + '.pdf'
#    os.system('start labels\\tuto1.pdf')