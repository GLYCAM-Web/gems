import gzip
import shutil
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from typing import Optional

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


RCSB_DOWNLOAD_BASE = "https://files.rcsb.org/download/"


def execute(pdb_id: str, output_dir, compressed: bool = False) -> Optional[Path]:
    """
    Download PDB file in standard PDB format from RCSB
    Args:
        pdb_id: 4-character PDB ID
        output_dir: Directory to save the file
        compressed: Download gzipped version if True
    Returns:
        Path to downloaded file or None if failed
    """
    pdb_id = pdb_id.lower()
    ext = ".pdb.gz" if compressed else ".pdb"
    filename = f"{pdb_id}{ext}"
    url = urljoin(RCSB_DOWNLOAD_BASE, filename)
    output_path = output_dir / filename
    
    try:
        with urlopen(url, timeout=30) as response:
            if response.status != 200:
                log.debug(f"Failed to download {pdb_id}: HTTP {response.status}")
                return None
            
            with open(output_path, 'wb') as f:
                shutil.copyfileobj(response, f)
        
        # Decompress if needed
        if compressed:
            decompressed_path = output_dir / f"{pdb_id}.pdb"
            with gzip.open(output_path, 'rb') as f_in:
                with open(decompressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            output_path.unlink()  # Remove compressed file
            output_path = decompressed_path
        
        log.debug(f"✓ Downloaded {pdb_id}.pdb to {output_path}")
        return output_path
        
    except HTTPError as e:
        log.debug(f"HTTP Error downloading {pdb_id}: {e.code} {e.reason}")
        return None
    except URLError as e:
        log.debug(f"URL Error downloading {pdb_id}: {e.reason}")
        return None
    except Exception as e:
        log.debug(f"Error downloading {pdb_id}: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        log.debug("Usage: python download_pdb.py <pdb_id> <output_dir> [compressed]")
        sys.exit(1)
    
    pdb_id = sys.argv[1]
    output_dir = Path(sys.argv[2])
    compressed = len(sys.argv) > 3 and sys.argv[3].lower() == "true"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    execute(pdb_id, output_dir, compressed)