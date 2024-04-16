####################################
# FONCTIONS NECESSAIRES AU PROJET  #
####################################

import os
import pandas as pd
from IPython.display import display, Markdown, clear_output
import panel as pn
import ipywidgets as widgets
import re
from sys import stdin               # how else should we get our input :)
from glob import glob
from bs4 import BeautifulSoup
from textacy.preprocessing.replace import urls

def remove_extra_spaces(text):
    """
    Remove extra spaces
    """
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()

def substitute_punctuations_with_white_space(text):
    """
    Substitute punctuations with white spaces in the input string.

    Parameters:
        text (str): The input string.

    Returns:
        str: The modified string with punctuations replaced by white spaces.
    """
    text = re.sub(r"[%s]" % re.escape('!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~“…”’'), " ", text)
    return text

def list_files_in_dir(path: str, filetype:str ='*.json'):
    """
    List files of a specific format in a directory
    """
    pattern = os.path.join(path, filetype)
    files = glob.glob(pattern)
    return files
    
def create_menu(df):
    menu = widgets.Dropdown(
       options=df.columns,
       value=df.columns[0],
       description='Mon texte :')
    return menu

def create_multiselect(df):
    multi_select = pn.widgets.MultiSelect(name='Mes variables :', value=[''],
    options=df.columns.to_list(), size=df.columns.size)
    return multi_select

# def create_corpus(df, message, l_variables,path):
#     new_df=pd.DataFrame()
#     i=0
#     for index, row in df.astype(str).iterrows():
#         first_line="**** "
#         for var in l_variables:
#             var_clean=clean_variable(var)
#             modalite=clean_modalite(row[var])
#             first_line= first_line + " *"+var_clean+"_"+modalite
#         second_line=row[message]
#         new_df.loc[i,'corpus']=first_line
#         i=i+1
#         new_df.loc[i,'corpus']=second_line
#         i=i+1
#     new_df.to_csv(os.path.join(path,"corpus.txt"), header=None, index=None, sep=';', mode='a')
#     return new_df

def create_corpus(df, message, l_variables):
    corpus_lines = []
    for _, row in df.astype(str).iterrows():
        first_line = ["****"]
        for var in l_variables:
            var_clean = clean_variable(var)
            modalite = clean_modalite(row[var])
            first_line.append("*{}_{}".format(var_clean, modalite))
        corpus_lines.extend([' '.join(first_line), row[message]])
        
    return corpus_lines

def clean_variable(var):
    var_clean=re.sub("[^a-zA-Z0-9]",'',var)
    return var_clean

def clean_modalite(var):
    var_clean=re.sub("[^a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ@#']",'-',var)
    var_clean = re.sub('-+', '', var_clean)
    return var_clean

def clean_text(text):
    if len(str(text)) >0:
        #On supprime les tags HTML
        text = BeautifulSoup(text,'html.parser').get_text()

        #On supprime les URLS
        text = urls(text , '')

        # normalization des onomatopées
        text = re.sub("\\b(a*ha+h[ha]*|o?l+o+l+[ol]*|e*he+h[he]*|i*hi+h[hi]*|u*hu+h[hu]*|o*ho+h[ho]*|é*hé+h[hé]*|u?l+u+l+[ul]*)\\b","lol", text,flags=re.MULTILINE );
        
        # suppression des mots et caractères répétés
        text = re.sub(r'([a-zA-Z])\1{2,}', r'\1', re.sub(r'\b(\w+)( \1\b)+', r'\1', text)) 
        
        #On met tout en minuscules, on supprime la ponctuation et les espaces en trop
        text = substitute_punctuations_with_white_space(text)
        text = text.lower()
        text = remove_extra_spaces(text)
    return text

# def clean_text (vTEXT):
#     if len(vTEXT) >1:
#         # suppression des urls
#         vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
#         vTEXT = re.sub("((0rz.tw)|(1link.in)|(1url.com)|(2.gp)|(2big.at)|(2tu.us)|(3.ly)|(307.to)|(4ms.me)|(4sq.com)|(4url.cc)|(6url.com)|(7.ly)|(a.gg)|(a.nf)|(aa.cx)|(abcurl.net)|(ad.vu)|(adf.ly)|(adjix.com)|(afx.cc)|(all.fuseurl.com)|(alturl.com)|(amzn.to)|(ar.gy)|(arst.ch)|(atu.ca)|(azc.cc)|(b23.ru)|(b2l.me)|(bacn.me)|(bcool.bz)|(binged.it)|(bit.ly)|(bizj.us)|(bloat.me)|(bravo.ly)|(bsa.ly)|(budurl.com)|(canurl.com)|(chilp.it)|(chzb.gr)|(cl.lk)|(cl.ly)|(clck.ru)|(cli.gs)|(cliccami.info)|(clickthru.ca)|(clop.in)|(conta.cc)|(cort.as)|(cot.ag)|(crks.me)|(ctvr.us)|(cutt.us)|(dai.ly)|(decenturl.com)|(dfl8.me)|(digbig.com)|(digg.com)|(disq.us)|(dld.bz)|(dlvr.it)|(do.my)|(doiop.com)|(dopen.us)|(easyuri.com)|(easyurl.net)|(eepurl.com)|(eweri.com)|(fa.by)|(fav.me)|(fb.me)|(fbshare.me)|(ff.im)|(fff.to)|(fire.to)|(firsturl.de)|(firsturl.net)|(flic.kr)|(flq.us)|(fly2.ws)|(fon.gs)|(freak.to)|(fuseurl.com)|(fuzzy.to)|(fwd4.me)|(fwib.net)|(g.ro.lt)|(gizmo.do)|(gl.am)|(go.9nl.com)|(go.ign.com)|(go.usa.gov)|(goo.gl)|(goshrink.com)|(gurl.es)|(hex.io)|(hiderefer.com)|(hmm.ph)|(href.in)|(hsblinks.com)|(htxt.it)|(huff.to)|(hulu.com)|(hurl.me)|(hurl.ws)|(icanhaz.com)|(idek.net)|(ilix.in)|(is.gd)|(its.my)|(ix.lt)|(j.mp)|(jijr.com)|(kl.am)|(klck.me)|(korta.nu)|(krunchd.com)|(l9k.net)|(lat.ms)|(liip.to)|(liltext.com)|(linkbee.com)|(linkbun.ch)|(liurl.cn)|(ln-s.net)|(ln-s.ru)|(lnk.gd)|(lnk.ms)|(lnkd.in)|(lnkurl.com)|(lru.jp)|(lt.tl)|(lurl.no)|(macte.ch)|(mash.to)|(merky.de)|(migre.me)|(miniurl.com)|(minurl.fr)|(mke.me)|(moby.to)|(moourl.com)|(mrte.ch)|(myloc.me)|(myurl.in)|(n.pr)|(nbc.co)|(nblo.gs)|(nn.nf)|(not.my)|(notlong.com)|(nsfw.in)|(nutshellurl.com)|(nxy.in)|(nyti.ms)|(o-x.fr)|(oc1.us)|(om.ly)|(omf.gd)|(omoikane.net)|(on.cnn.com)|(on.mktw.net)|(onforb.es)|(orz.se)|(ow.ly)|(ping.fm)|(pli.gs)|(pnt.me)|(politi.co)|(post.ly)|(pp.gg)|(profile.to)|(ptiturl.com)|(pub.vitrue.com)|(qlnk.net)|(qte.me)|(qu.tc)|(qy.fi)|(r.im)|(rb6.me)|(read.bi)|(readthis.ca)|(reallytinyurl.com)|(redir.ec)|(redirects.ca)|(redirx.com)|(retwt.me)|(ri.ms)|(rickroll.it)|(riz.gd)|(rt.nu)|(ru.ly)|(rubyurl.com)|(rurl.org)|(rww.tw)|(s4c.in)|(s7y.us)|(safe.mn)|(sameurl.com)|(sdut.us)|(shar.es)|(shink.de)|(shorl.com)|(short.ie)|(short.to)|(shortlinks.co.uk)|(shorturl.com)|(shout.to)|(show.my)|(shrinkify.com)|(shrinkr.com)|(shrt.fr)|(shrt.st)|(shrten.com)|(shrunkin.com)|(simurl.com)|(slate.me)|(smallr.com)|(smsh.me)|(smurl.name)|(sn.im)|(snipr.com)|(snipurl.com)|(snurl.com)|(sp2.ro)|(spedr.com)|(srnk.net)|(srs.li)|(starturl.com)|(su.pr)|(surl.co.uk)|(surl.hu)|(t.cn)|(t.co)|(t.lh.com)|(ta.gd)|(tbd.ly)|(tcrn.ch)|(tgr.me)|(tgr.ph)|(tighturl.com)|(tiniuri.com)|(tiny.cc)|(tiny.ly)|(tiny.pl)|(tinylink.in)|(tinyuri.ca)|(tinyurl.com)|(tl.gd)|(tmi.me)|(tnij.org)|(tnw.to)|(tny.com)|(to.ly)|(togoto.us)|(totc.us)|(toysr.us)|(tpm.ly)|(tr.im)|(tra.kz)|(trunc.it)|(twhub.com)|(twirl.at)|(twitclicks.com)|(twitterurl.net)|(twitterurl.org)|(twiturl.de)|(twurl.cc)|(twurl.nl)|(u.mavrev.com)|(u.nu)|(u76.org)|(ub0.cc)|(ulu.lu)|(updating.me)|(ur1.ca)|(url.az)|(url.co.uk)|(url.ie)|(url360.me)|(url4.eu)|(urlborg.com)|(urlbrief.com)|(urlcover.com)|(urlcut.com)|(urlenco.de)|(urli.nl)|(urls.im)|(urlshorteningservicefortwitter.com)|(urlx.ie)|(urlzen.com)|(usat.ly)|(use.my)|(vb.ly)|(vgn.am)|(vl.am)|(vm.lc)|(w55.de)|(wapo.st)|(wapurl.co.uk)|(wipi.es)|(wp.me)|(x.vu)|(xr.com)|(xrl.in)|(xrl.us)|(xurl.es)|(xurl.jp)|(y.ahoo.it)|(yatuc.com)|(ye.pe)|(yep.it)|(yfrog.com)|(yhoo.it)|(yiyd.com)|(youtu.be)|(yuarel.com)|(z0p.de)|(zi.ma)|(zi.mu)|(zipmyurl.com)|(zud.me)|(zurl.ws)|(zz.gd)|(zzang.kr)/([a-zA-Z0-9]))","", vTEXT, flags=re.MULTILINE)
#         # normalization des onomatopées
#         vTEXT = re.sub("\\b(a*ha+h[ha]*|o?l+o+l+[ol]*|e*he+h[he]*|i*hi+h[hi]*|u*hu+h[hu]*|o*ho+h[ho]*|é*hé+h[hé]*|u?l+u+l+[ul]*)\\b","lol", vTEXT,flags=re.MULTILINE );
#         # suppression des mots répétés
#         vTEXT = re.sub(r'\b(\w+)( \1\b)+', r'\1', vTEXT)
#         # suppression des caractères répétés
#         vTEXT = re.sub(r'([a-zA-Z])\1{2,}', r'\1', vTEXT)  
#         # suppression des espaces répétés
#         vTEXT = re.sub(' +', ' ', vTEXT)
#     return(vTEXT)
