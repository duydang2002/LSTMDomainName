from datetime import datetime
import random
from dga_classifier.dga_generators import banjori, corebot, cryptolocker, \
    dircrypt, kraken, lockyv2, pykspa, qakbot, ramdo, ramnit, simda
domains = []
labels = []
num_per_dga = 5
# We use some arbitrary seeds to create domains with banjori
banjori_seeds = ['somestring', 'firetruck', 'bulldozer', 'airplane', 'racecar',
                    'apartment', 'laptop', 'laptopcomp', 'malwareisbad', 'crazytrain',
                    'thepolice', 'fivemonkeys', 'hockey', 'football', 'baseball',
                    'basketball', 'trackandfield', 'fieldhockey', 'softball', 'redferrari',
                    'blackcheverolet', 'yellowelcamino', 'blueporsche', 'redfordf150',
                    'purplebmw330i', 'subarulegacy', 'hondacivic', 'toyotaprius',
                    'sidewalk', 'pavement', 'stopsign', 'trafficlight', 'turnlane',
                    'passinglane', 'trafficjam', 'airport', 'runway', 'baggageclaim',
                    'passengerjet', 'delta1008', 'american765', 'united8765', 'southwest3456',
                    'albuquerque', 'sanfrancisco', 'sandiego', 'losangeles', 'newyork',
                    'atlanta', 'portland', 'seattle', 'washingtondc']

segs_size = int(max(1, num_per_dga/len(banjori_seeds)))

for banjori_seed in banjori_seeds:
    domains += banjori.generate_domains(int(segs_size), banjori_seed)
    labels += ['banjori']*segs_size

domains += corebot.generate_domains(num_per_dga)
labels += ['corebot']*num_per_dga

# Create different length domains using cryptolocker
crypto_lengths = range(8, 32)
segs_size = int(max(1, num_per_dga/len(crypto_lengths)))
for crypto_length in crypto_lengths:
    domains += cryptolocker.generate_domains(segs_size,
                                                seed_num=random.randint(1, 1000000),
                                                length=crypto_length)
    labels += ['cryptolocker']*segs_size

domains += dircrypt.generate_domains(num_per_dga)
labels += ['dircrypt']*num_per_dga

# generate kraken and divide between configs
kraken_to_gen = int(max(1, num_per_dga/2))
domains += kraken.generate_domains(kraken_to_gen, datetime(2023, 1, 1), 'a', 3)
labels += ['kraken']*kraken_to_gen
domains += kraken.generate_domains(kraken_to_gen, datetime(2016, 1, 1), 'b', 3)
labels += ['kraken']*kraken_to_gen

# generate locky and divide between configs
locky_gen = int(max(1, num_per_dga/11))
for i in range(1, 12):
    domains += lockyv2.generate_domains(locky_gen, config=i)
    labels += ['locky']*locky_gen

# Generate pyskpa domains
domains += pykspa.generate_domains(num_per_dga, datetime(2016, 1, 1))
labels += ['pykspa']*num_per_dga

# Generate qakbot
domains += qakbot.generate_domains(num_per_dga, tlds=[])
labels += ['qakbot']*num_per_dga

# ramdo divided over different lengths
ramdo_lengths = range(8, 32)
segs_size = int(max(1, num_per_dga/len(ramdo_lengths)))
for rammdo_length in ramdo_lengths:
    domains += ramdo.generate_domains(segs_size,
                                        seed_num=random.randint(1, 1000000),
                                        length=rammdo_length)
    labels += ['ramdo']*segs_size

# ramnit
domains += ramnit.generate_domains(num_per_dga, 0x123abc12)
labels += ['ramnit']*num_per_dga

# simda
simda_lengths = range(8, 32)
segs_size = int(max(1, num_per_dga/len(simda_lengths)))
for simda_length in range(len(simda_lengths)):
    domains += simda.generate_domains(segs_size,
                                        length=simda_length,
                                        tld=None,
                                        base=random.randint(2, 2**32))
    labels += ['simda']*segs_size
for label, domains  in zip(labels, domains ):
    print(f"Label: {label} Domains : {domains} " )