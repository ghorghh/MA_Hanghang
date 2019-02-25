#Class IO
import logging
import time
import os
import struct
import xlwt
import socket
from xlrd import open_workbook
from xlutils.copy import copy
class myio:
    def __init__(self, serverName, serverPort):
        self.target_path = '/home/pi/ghh/Log'
        self.akku_id = ''

        self.unten_obIO = False;
        self.mittel_obIO = False;
        self.oben_obIO = False;

        self.deckel_erstmal_gefunden = False;

        self.unten_time = '0'
        self.mittel_time = '0'
        self.oben_time = '0'


        self.serverName = serverName
        self.serverPort = serverPort



        self.mytime = time.strftime('%Y%m%d',time.localtime())
        self.myexcel = self.mytime + '.xls'

        self.style1 = ('Arial', 250, True, False, 'green')
        self.style2 = ('Arial', 200, False, False, 'white')
        self.style3 = ('Arial', 200, False, True, 'red')

    def get_time(self):
        ebene_time = time.strftime('%H%M%S', time.localtime())
        return ebene_time

    def file_set(self):

        if not os.path.exists(self.target_path):
            os.mkdir(self.target_path)
        os.chdir(self.target_path)

        if not os.path.isdir(self.mytime):
            os.mkdir(self.mytime)

        os.chdir(self.target_path + '/' + self.mytime)
        ispath = os.getcwd()
        logging.info('Path is: {}'.format(ispath))

        if not os.path.isfile(self.myexcel):
            self.myexcel_creation()

    def myexcel_creation(self):
        book = xlwt.Workbook()
        sheet1 = book.add_sheet(self.mytime)
        sheet1.write_merge(0, 1, 0, 2, 'AkkuGruppe_ID', self.get_style_title())
        sheet1.write_merge(0, 1, 3, 4, 'Unten_Ebene', self.get_style_title())
        sheet1.write_merge(0, 1, 5, 6, 'Schluss_Zeit (UG)', self.get_style_title())
        sheet1.write_merge(0, 1, 7, 8, 'Mittel_Ebene', self.get_style_title())
        sheet1.write_merge(0, 1, 9, 10, 'Schluss_Zeit (MG)', self.get_style_title())
        sheet1.write_merge(0, 1, 11, 12, 'Oben_Ebene', self.get_style_title())
        sheet1.write_merge(0, 1, 13, 14, 'Schluss_Zeit (OG)', self.get_style_title())
        sheet1.write_merge(0, 1, 15, 17, 'ob_In_Ordnung', self.get_style_title())
        book.save(self.myexcel)

    def get_style_title(self):
        style_title = self.set_excel_style(self.style1[0], self.style1[1], self.style1[2], self.style1[3], self.style1[4])
        return style_title
    def get_style_true(self):
        style_true = self.set_excel_style(self.style2[0], self.style2[1], self.style2[2], self.style2[3], self.style2[4])
        return style_true
    def get_style_false(self):
        style_false = self.set_excel_style(self.style3[0], self.style3[1], self.style3[2], self.style3[3], self.style3[4])
        return style_false
    
    def set_excel_style(self, name, height, bold, mypattern, back_color):
        style = xlwt.XFStyle()

        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER

        pattern = xlwt.Pattern()
        if mypattern == True:
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        else:
            pattern.pattern = xlwt.Pattern.NO_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map[back_color]

        borders = xlwt.Borders()
        borders.left = borders.MEDIUM
        borders.right = borders.MEDIUM
        borders.top = borders.MEDIUM
        borders.bottom = borders.MEDIUM

        style.font = font
        style.alignment = alignment
        style.pattern = pattern
        style.borders = borders
        
        return style        

    def io_manipulation(self, data_struct, client1, akku_id):
##        print(data_struct)
        self.akku_id = akku_id
        
        deckel = data_struct[11]
##        print(type(data_struct[1]))
        
        #excel style
        style_title = self.get_style_title()
        style_true = self.get_style_true()
        style_false = self.get_style_false()
        
        unten_ebene = data_struct[14]
        mittel_ebene = data_struct[15]
        oben_ebene = data_struct[16]

        if data_struct[17] == 1:
            self.unten_obIO = True
        if data_struct[17] == 2:
            self.unten_obIO = False
        if data_struct[18] == 1:
            self.mittel_obIO = True
        if data_struct[18] == 2:
            self.mittel_obIO = False
        if data_struct[19] == 1:
            self.oben_obIO = True
        if data_struct[19] == 2:
            self.oben_obIO = False
        ##if deckel gefunden ist, schreiben die Daten ins Excel einmal ein.
        if deckel == True and self.deckel_erstmal_gefunden == False and (self.unten_time != '0' and self.mittel_time != '0' and self.oben_time != '0'):
            self.deckel_erstmal_gefunden = True;

            #open excel
            rexcel = open_workbook(self.myexcel, formatting_info = True)
            #read lines
            line = rexcel.sheet_by_name(self.mytime).nrows
##            print(line, type(line))
            #change to xlwt
            book = copy(rexcel)
            sheet1 = book.get_sheet(self.mytime)
            sheet1.write_merge(line, line, 0, 2, self.akku_id, style_true)
            if self.unten_obIO == False:
                sheet1.write_merge(line, line, 3, 4, 'False', style_false)
            else:
                sheet1.write_merge(line, line, 3, 4, 'True', style_true)
                
            sheet1.write_merge(line, line, 5, 6, self.unten_time[0:2] + ':' + self.unten_time[2:4] + ':' + self.unten_time[4:6], style_true)
            
            if self.mittel_obIO == False:
                sheet1.write_merge(line, line, 7, 8, 'False', style_false)
            else:
                sheet1.write_merge(line, line, 7, 8, 'True', style_true)
                
            sheet1.write_merge(line, line, 9, 10, self.mittel_time[0:2] + ':' + self.mittel_time[2:4] + ':' + self.mittel_time[4:6], style_true)
            
            if self.oben_obIO == False:
                sheet1.write_merge(line, line, 11, 12, 'False', style_false)
            else:
                sheet1.write_merge(line, line, 11, 12, 'True', style_true)
                
            sheet1.write_merge(line, line, 13, 14, self.oben_time[0:2] + ':' + self.oben_time[2:4] + ':' + self.oben_time[4:6], style_true)

            if self.unten_obIO and self.mittel_obIO and self.oben_obIO:
                sheet1.write_merge(line, line, 15, 17, 'I.O', style_true)
            else:
                sheet1.write_merge(line, line, 15, 17, 'n.I.O', style_false)

            book.save(self.myexcel)

            ##reset time variable
            self.unten_time = '0'
            self.mittel_time = '0'
            self.oben_time = '0'

        if deckel == False:
            self.deckel_erstmal_gefunden = False
                
            #get time information,write it to variable
            if unten_ebene == True and mittel_ebene == False and oben_ebene == False:
                self.unten_time = self.get_time()                  

            if mittel_ebene == True and oben_ebene == False and unten_ebene == False:
                self.mittel_time = self.get_time()

            if oben_ebene ==True and mittel_ebene == False and unten_ebene == False:
                self.oben_time = self.get_time()

        else:
            pass

        
        

    
