#!/usr/bin/env python3
"""Package all nine runtime folders, individual downloads and one combined ZIP."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
ARCHIVES={'Eida':'Eida_DAEMON_ORIGINAL.zip','PochitaTrueForm':'PochitaTrueForm_ACABADO.zip','Mamushi':'Mamushi_SHINJU.zip','Shibai':'Shibai_OTSUTSUKI.zip','JuraShinju':'JuraShinju.zip','MitsukiTBV':'MitsukiTBV.zip','RyuShinju':'RyuShinju.zip','HidariShinju':'HidariShinju.zip','MatsuriShinju':'MatsuriShinju.zip'}
VALIDATORS=dict(zip(ARCHIVES,['character','pochita','mamushi','shibai','jura','mitsuki','ryu','hidari','matsuri']))
ALIASES={'Eida':['Eida_ULTI_SPRITES_ORIGINALES.zip','Eida_SONIDO_Y_ABRAZO.zip','Eida_ACABADO.zip','Eida_COREOGRAFIA_Y_OMNIPOTENCIA.zip','Eida_FIX3_DERRIBO_Y_COMBOS.zip','Eida_FIX2_CMD304.zip','Eida_FIX_CARGA_MUGEN11.zip','Eida_OMNIPOTENCIA_COMBOS.zip'],
         'PochitaTrueForm':['PochitaTrueForm.zip','PochitaTrueForm_AEREOS_Y_BUFANDA.zip','PochitaTrueForm_SIN_SIERRA_GIGANTE.zip','PochitaTrueForm_DESPERTAR_Y_BORRADO.zip','PochitaTrueForm_ESPECIALES_LARGOS.zip','PochitaTrueForm_ESPECIALES_CON_SONIDO.zip','PochitaTrueForm_JUGABILIDAD.zip','PochitaTrueForm_CORREGIDO.zip','PochitaTrueForm_REMATES.zip']}
def digest(data):return hashlib.sha256(data).hexdigest()
def write(z,name,data):
    info=ZipInfo(name,(2026,10,24,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
    z.writestr(info,data,compresslevel=9)
def main():
    reports={};contents={}
    for ch,filename in ARCHIVES.items():
        files={p.name:p.read_bytes() for p in sorted((ROOT/ch).iterdir()) if p.is_file() and p.suffix in ['.def','.cns','.cmd','.air','.sff','.snd','.md']}
        contents[ch]=files;path=ROOT/filename
        with ZipFile(path,'w',ZIP_DEFLATED,compresslevel=9) as z:
            for name,data in files.items():write(z,ch+'/'+name,data)
        with tempfile.TemporaryDirectory(prefix='roster-artifact-') as tmp:
            with ZipFile(path) as z:
                assert z.testzip() is None;z.extractall(tmp)
                assert all(z.read(ch+'/'+name)==data for name,data in files.items())
            r=subprocess.run([sys.executable,str(ROOT/'tools'/('validate_'+VALIDATORS[ch]+'.py')),str(Path(tmp)/ch)],capture_output=True,text=True)
            assert r.returncode==0,r.stdout+r.stderr
        for alias in ALIASES.get(ch,[]):shutil.copyfile(path,ROOT/alias)
        reports[ch]=dict(archive=filename,bytes=path.stat().st_size,sha256=digest(path.read_bytes()),files={n:digest(d) for n,d in files.items()},extracted_validation=True)
        print(filename,path.stat().st_size,'bytes; extracted validation passed',flush=True)
    instructions='''PERSONAJES CORREGIDOS — 24/10/2026

1. Cierra MUGEN y guarda una copia de las carpetas antiguas si quieres conservarlas.
2. Copia las nueve carpetas de este ZIP dentro de la carpeta chars de tu juego,
   sustituyendo las versiones anteriores de esos mismos personajes.
3. En data/select.def, dentro de [Characters], usa estas entradas si aún no existen:

'''+''.join(ch+'/'+ch+'.def\n' for ch in ARCHIVES)+'''
Evita añadir una segunda entrada del mismo personaje. Jura se llama JuraShinju
para que pueda coexistir con otro personaje llamado Jura.

Los controles, créditos y notas de la revisión están dentro de cada carpeta.
Se conservan los movimientos, las ultis con gasto de energía y sus límites de daño.
Las pruebas se realizaron en Ikemen GO con sintaxis de MUGEN 1.1; la instalación
concreta de Jump Force MUGEN V14 requiere comprobación local.
'''
    bundle=ROOT/'Personajes_CORREGIDOS.zip'
    with ZipFile(bundle,'w',ZIP_DEFLATED,compresslevel=9) as z:
        write(z,'INSTALACION.txt',instructions.encode())
        for ch,files in contents.items():
            for name,data in files.items():write(z,ch+'/'+name,data)
    with ZipFile(bundle) as z:
        assert z.testzip() is None
        assert all(z.read(ch+'/'+n)==d for ch,files in contents.items() for n,d in files.items())
    result=dict(archives=reports,bundle=dict(archive=bundle.name,bytes=bundle.stat().st_size,sha256=digest(bundle.read_bytes()),all_runtime_bytes_verified=True))
    (ROOT/'previews/roster_delivery_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(bundle.name,bundle.stat().st_size,'bytes; all nine runtimes verified')
if __name__=='__main__':main()
