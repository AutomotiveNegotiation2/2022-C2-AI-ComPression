#!/bin/bash
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1jxuDXnDGQOhBEzTaVSTRj2ktUGDkY73S' -O weight.tar
tar -xvf weight.tar
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=13R9MYMNsqI4E1CMpHuO-lRh5n3lHirDa' -O can_cfg.tar
tar -xvf can_cfg.tar