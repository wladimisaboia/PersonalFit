from django.core.management.base import BaseCommand
from pe_evaluation.models import PredefinedTraining

class Command(BaseCommand):
    help = 'Popula o banco de dados com treinos pré-determinados'

    def handle(self, *args, **kwargs):
        trainings = [
            # Homens Adultos - Emagrecimento
            {
                'profile': 'homem_adulto',
                'level': 'iniciante',
                'goal': 'Emagrecimento',
                'description': "Alta Intensidade (Moderada): Supino Máquina – 2 séries de 12 (carga leve), Puxada Frontal – 2 séries de 12 (carga leve), Agachamento Livre – 2 séries de 10 (peso corporal), Remada Unilateral com Halteres – 2 séries de 12, Burpees – 2 séries de 8 repetições, Caminhada Rápida na Esteira – 15 min"
            },
            {
                'profile': 'homem_adulto',
                'level': 'intermediario',
                'goal': 'Emagrecimento',
                'description': "Alta Intensidade: Supino Máquina – 3 séries de 12 (carga moderada), Puxada Frontal – 3 séries de 12, Agachamento com Barra – 3 séries de 12 (peso leve a moderado), Remada Baixa na Polia – 3 séries de 12, Burpees – 3 séries de 12 repetições (ou 30 seg), Bicicleta Ergométrica (HIIT) – 10 min (30 seg forte / 30 seg leve)"
            },
            {
                'profile': 'homem_adulto',
                'level': 'avancado',
                'goal': 'Emagrecimento',
                'description': "Alta Intensidade: Supino Inclinado com Barra – 4 séries de 10 (carga moderada a pesada), Puxada Frontal – 4 séries de 10, Agachamento com Barra – 4 séries de 10 (carga moderada a pesada), Remada Cavalinho – 4 séries de 10, Burpees – 4 séries de 15 repetições, Corrida na Esteira (HIIT) – 15 min (1 min forte / 1 min leve)"
            },
            # Homens Idosos - Emagrecimento
            {
                'profile': 'homem_idoso',
                'level': 'iniciante',
                'goal': 'Emagrecimento',
                'description': "Moderada Intensidade: Caminhada na Esteira – 10 min (ritmo confortável), Supino Máquina – 2 séries de 12 (carga leve), Puxada Frontal – 2 séries de 12 (carga leve), Agachamento Assistido (com cadeira) – 2 séries de 10 (peso corporal), Elevação de Pernas na Cadeira (para core) – 2 séries de 10, Bicicleta Ergométrica – 10 min (ritmo leve a moderado)"
            },
            {
                'profile': 'homem_idoso',
                'level': 'intermediario',
                'goal': 'Emagrecimento',
                'description': "Moderada a Alta Intensidade: Caminhada Rápida ou Leve Inclinação na Esteira – 12 min, Supino Máquina – 3 séries de 12 (carga moderada), Puxada Frontal – 3 séries de 12 (carga moderada), Agachamento Livre (sem apoio) – 3 séries de 12 (peso corporal ou leve), Remada Baixa na Polia – 3 séries de 12, Bicicleta Ergométrica (Intercalada) – 10 min (1 min leve / 1 min moderado)"
            },
            {
                'profile': 'homem_idoso',
                'level': 'avancado',
                'goal': 'Emagrecimento',
                'description': "Alta Intensidade Controlada: Caminhada com Inclinação ou Corrida Leve na Esteira – 15 min, Supino Inclinado com Halteres – 4 séries de 10 (carga moderada a pesada), Puxada Frontal – 4 séries de 10 (carga moderada a pesada), Agachamento com Halteres – 4 séries de 10 (peso leve a moderado), Remada Unilateral com Halteres – 4 séries de 10 (carga moderada), Bicicleta Ergométrica (HIIT) – 12 min (30 seg forte / 1 min leve)"
            },
            # Mulheres Adultas - Emagrecimento
            {
                'profile': 'mulher_adulta',
                'level': 'iniciante',
                'goal': 'Emagrecimento',
                'description': "Moderada Intensidade: Caminhada Rápida na Esteira – 10 min (ritmo confortável), Agachamento com Bola Suíça na Parede – 2 séries de 12 (peso corporal), Puxada Frontal – 2 séries de 12 (carga leve), Supino Máquina – 2 séries de 12 (carga leve), Elevação de Quadril (Glúteos) – 2 séries de 15, Bicicleta Ergométrica – 10 min (ritmo moderado)"
            },
            {
                'profile': 'mulher_adulta',
                'level': 'intermediario',
                'goal': 'Emagrecimento',
                'description': "Moderada a Alta Intensidade: Caminhada Rápida ou Inclinação Leve na Esteira – 12 min, Agachamento com Halteres – 3 séries de 12 (peso leve a moderado), Puxada Frontal – 3 séries de 12 (carga moderada), Supino Máquina – 3 séries de 12 (carga moderada), Avanço (Lunges) com Halteres – 3 séries de 10 (cada perna), Bicicleta Ergométrica (Intercalada) – 12 min (1 min leve / 1 min moderado)"
            },
            {
                'profile': 'mulher_adulta',
                'level': 'avancado',
                'goal': 'Emagrecimento',
                'description': "Alta Intensidade: Corrida na Esteira (HIIT) – 15 min (30 seg forte / 30 seg leve), Agachamento com Barra – 4 séries de 10 (peso moderado a pesado), Puxada Frontal – 4 séries de 10 (carga moderada a pesada), Supino Inclinado com Halteres – 4 séries de 10 (carga moderada a pesada), Avanço Dinâmico com Halteres – 4 séries de 12 (cada perna), Burpees – 3 séries de 15 repetições"
            },
            # Mulheres Idosas - Emagrecimento
            {
                'profile': 'mulher_idosa',
                'level': 'iniciante',
                'goal': 'Emagrecimento',
                'description': "Moderada Intensidade: Caminhada na Esteira – 10 min (ritmo confortável), Agachamento Assistido (com apoio de cadeira) – 2 séries de 10 (peso corporal), Remada Baixa na Polia – 2 séries de 12 (carga leve), Elevação de Quadril (Glúteos) – 2 séries de 15, Supino Máquina – 2 séries de 12 (carga leve), Bicicleta Ergométrica – 10 min (ritmo leve a moderado)"
            },
            {
                'profile': 'mulher_idosa',
                'level': 'intermediario',
                'goal': 'Emagrecimento',
                'description': "Moderada Intensidade: Caminhada Rápida na Esteira ou Inclinação Leve – 12 min, Agachamento Livre (sem apoio) – 3 séries de 12 (peso corporal ou leve), Remada Unilateral com Halteres – 3 séries de 12 (carga leve a moderada), Elevação de Quadril com Carga Leve – 3 séries de 15, Supino Máquina – 3 séries de 12 (carga moderada), Bicicleta Ergométrica – 12 min (1 min moderado / 1 min leve)"
            },
            {
                'profile': 'mulher_idosa',
                'level': 'avancado',
                'goal': 'Emagrecimento',
                'description': "Alta Intensidade Controlada: Caminhada Rápida na Esteira com Inclinação – 15 min (ou leve trote, se possível), Agachamento com Halteres – 4 séries de 10 (carga leve a moderada), Remada Cavalinho – 4 séries de 10 (carga moderada), Elevação de Quadril Unilateral – 3 séries de 12 (cada perna, com peso leve), Supino Inclinado com Halteres – 4 séries de 10 (carga moderada a pesada), Bicicleta Ergométrica (HIIT) – 12 min (30 seg forte / 1 min leve)"
            },
            # Homens Adultos - Ganho de Massa Muscular
            {
                'profile': 'homem_adulto',
                'level': 'iniciante',
                'goal': 'Ganho de Massa Muscular',
                'description': "Moderada Intensidade: Supino Máquina – 3 séries de 12 (carga leve a moderada), Puxada Frontal – 3 séries de 12 (carga leve a moderada), Agachamento Livre com Peso Corporal – 3 séries de 10, Desenvolvimento com Halteres (ombros) – 3 séries de 12, Rosca Direta com Halteres – 3 séries de 12 (carga leve), Bicicleta Ergométrica – 5 min de aquecimento (ritmo leve)"
            },
            {
                'profile': 'homem_adulto',
                'level': 'intermediario',
                'goal': 'Ganho de Massa Muscular',
                'description': "Moderada a Alta Intensidade: Supino com Barra – 4 séries de 10 (carga moderada), Puxada Fechada na Polia – 4 séries de 10 (carga moderada), Agachamento com Barra – 4 séries de 10 (peso moderado), Desenvolvimento com Halteres – 4 séries de 10 (carga moderada), Rosca Martelo – 4 séries de 10 (carga moderada), Abdominais na Máquina – 3 séries de 15"
            },
            {
                'profile': 'homem_adulto',
                'level': 'avancado',
                'goal': 'Ganho de Massa Muscular',
                'description': "Alta Intensidade: Supino Reto com Barra – 5 séries de 8 (carga moderada a pesada), Remada Curvada com Barra – 5 séries de 8 (carga moderada a pesada), Agachamento Profundo com Barra – 5 séries de 8 (carga moderada a pesada), Desenvolvimento Militar com Barra – 4 séries de 8 (carga moderada a pesada), Rosca Concentrada com Halteres – 4 séries de 10 (carga moderada), Abdominais com Carga (anilha no peito) – 3 séries de 12"
            },
            # Homens Idosos - Ganho de Massa Muscular
            {
                'profile': 'homem_idoso',
                'level': 'iniciante',
                'goal': 'Ganho de Massa Muscular',
                'description': "Baixa a Moderada Intensidade: Supino Máquina – 3 séries de 10 (carga leve), Remada Baixa na Polia – 3 séries de 10 (carga leve), Agachamento Assistido (com apoio de cadeira ou barra) – 3 séries de 10 (peso corporal), Desenvolvimento com Halteres (sentado) – 3 séries de 12 (carga leve), Rosca Direta com Halteres – 3 séries de 12 (carga leve), Extensão de Tríceps com Halter – 3 séries de 12 (carga leve)"
            },
            {
                'profile': 'homem_idoso',
                'level': 'intermediario',
                'goal': 'Ganho de Massa Muscular',
                'description': "Moderada Intensidade: Supino Inclinado com Halteres – 4 séries de 10 (carga moderada), Remada Unilateral com Halteres – 4 séries de 10 (carga moderada), Agachamento com Halteres – 4 séries de 10 (peso moderado), Desenvolvimento com Halteres (sentado) – 4 séries de 10 (carga moderada), Rosca Alternada com Halteres – 4 séries de 10 (carga moderada), Extensão de Tríceps na Polia – 4 séries de 12 (carga moderada)"
            },
            {
                'profile': 'homem_idoso',
                'level': 'avancado',
                'goal': 'Ganho de Massa Muscular',
                'description': "Alta Intensidade Controlada: Supino Reto com Barra – 5 séries de 8 (carga moderada a pesada), Remada Cavalinho – 5 séries de 8 (carga moderada a pesada), Agachamento com Barra (profundidade controlada) – 5 séries de 8 (carga moderada a pesada), Desenvolvimento Militar com Halteres – 4 séries de 8 (carga moderada a pesada), Rosca Concentrada com Halter – 4 séries de 10 (carga moderada), Extensão de Tríceps com Halter (sobre a cabeça) – 4 séries de 10 (carga moderada)"
            },
            # Mulheres Adultas - Ganho de Massa Muscular
            {
                'profile': 'mulher_adulta',
                'level': 'iniciante',
                'goal': 'Ganho de Massa Muscular',
                'description': "Baixa a Moderada Intensidade: Agachamento Livre (peso corporal ou halteres leves) – 3 séries de 10, Supino Máquina – 3 séries de 10 (carga leve), Remada Baixa na Polia – 3 séries de 10 (carga leve), Elevação de Quadril (Glúteos) – 3 séries de 12 (peso corporal ou carga leve), Desenvolvimento com Halteres (ombros) – 3 séries de 12 (carga leve), Rosca Direta com Halteres – 3 séries de 12 (carga leve)"
            },
            {
                'profile': 'mulher_adulta',
                'level': 'intermediario',
                'goal': 'Ganho de Massa Muscular',
                'description': "Moderada Intensidade: Agachamento com Halteres – 4 séries de 10 (carga moderada), Supino Inclinado com Halteres – 4 séries de 10 (carga moderada), Remada Unilateral com Halteres – 4 séries de 10 (carga moderada), Elevação de Quadril com Barra – 4 séries de 12 (carga moderada), Desenvolvimento com Halteres (sentado) – 4 séries de 10 (carga moderada), Rosca Martelo com Halteres – 4 séries de 10 (carga moderada)"
            },
            {
                'profile': 'mulher_adulta',
                'level': 'avancado',
                'goal': 'Ganho de Massa Muscular',
                'description': "Alta Intensidade: Agachamento Livre com Barra – 5 séries de 8 (carga moderada a pesada), Supino Reto com Barra – 5 séries de 8 (carga moderada a pesada), Remada Curvada com Barra – 5 séries de 8 (carga moderada a pesada), Elevação de Quadril com Barra Pesada – 4 séries de 10, Desenvolvimento Militar com Halteres – 4 séries de 8 (carga moderada a pesada), Rosca Concentrada com Halteres – 4 séries de 10 (carga moderada)"
            },
            # Mulheres Idosas - Ganho de Massa Muscular
            {
                'profile': 'mulher_idosa',
                'level': 'iniciante',
                'goal': 'Ganho de Massa Muscular',
                'description': "Baixa Intensidade: Agachamento Assistido (com apoio de cadeira ou barra) – 3 séries de 10, Supino Máquina – 3 séries de 10 (carga leve), Remada Baixa na Polia – 3 séries de 10 (carga leve), Elevação de Quadril (Glúteos) – 3 séries de 12 (peso corporal ou carga leve), Desenvolvimento com Halteres (sentado) – 3 séries de 12 (carga leve), Rosca Direta com Halteres – 3 séries de 12 (carga leve)"
            },
            {
                'profile': 'mulher_idosa',
                'level': 'intermediario',
                'goal': 'Ganho de Massa Muscular',
                'description': "Moderada Intensidade: Agachamento com Halteres – 4 séries de 10 (carga moderada), Supino Inclinado com Halteres – 4 séries de 10 (carga moderada), Remada Unilateral com Halteres – 4 séries de 10 (carga moderada), Elevação de Quadril com Peso – 4 séries de 12 (carga moderada), Desenvolvimento com Halteres (sentado) – 4 séries de 10 (carga moderada), Rosca Martelo com Halteres – 4 séries de 10 (carga moderada)"
            },
            {
                'profile': 'mulher_idosa',
                'level': 'avancado',
                'goal': 'Ganho de Massa Muscular',
                'description': "Alta Intensidade Controlada: Agachamento com Barra – 5 séries de 8 (carga moderada a pesada), Supino Reto com Barra – 5 séries de 8 (carga moderada a pesada), Remada Curvada com Barra – 5 séries de 8 (carga moderada a pesada), Elevação de Quadril com Barra Pesada – 4 séries de 10, Desenvolvimento Militar com Halteres – 4 séries de 8 (carga moderada a pesada), Rosca Concentrada com Halteres – 4 séries de 10 (carga moderada)"
            },

            # Homens Adultos - Condicionamento Físico
            {
                'profile': 'homem_adulto',
                'level': 'iniciante',
                'goal': 'Condicionamento Físico',
                'description': "Baixa Intensidade: Caminhada Rápida ou Caminhada na Esteira – 20 minutos, Agachamento Livre (peso corporal) – 3 séries de 12, Flexões de Braço (com apoio de joelhos, se necessário) – 3 séries de 8 a 12, Remada Baixa na Polia (carga leve) – 3 séries de 10, Abdominais (crunches) – 3 séries de 12, Bicicleta Ergométrica – 10 minutos em intensidade moderada"
            },
            {
                'profile': 'homem_adulto',
                'level': 'intermediario',
                'goal': 'Condicionamento Físico',
                'description': "Moderada Intensidade: Corrida Leve ou na Esteira – 20 minutos, Agachamento com Halteres – 4 séries de 10, Flexões de Braço (normais) – 4 séries de 10 a 15, Remada Unilateral com Halteres – 4 séries de 10, Abdominais (prancha) – 4 séries de 30 segundos, Bicicleta Ergométrica (HIIT) – 15 minutos (30 seg forte / 30 seg leve)"
            },
            {
                'profile': 'homem_adulto',
                'level': 'avancado',
                'goal': 'Condicionamento Físico',
                'description': "Alta Intensidade: Corrida Intercalada (sprints) – 25 minutos (alternar entre 1 min rápido / 2 min leve), Agachamento com Barra – 5 séries de 8 (carga moderada a pesada), Flexões de Braço (com aumento de intensidade, como flexões declinadas) – 5 séries de 12, Remada Curvada com Barra – 5 séries de 8 a 10 (carga moderada a pesada), Abdominais (prancha com elevação de pernas) – 5 séries de 45 segundos, Bicicleta Ergométrica (HIIT) – 20 minutos (30 seg forte / 30 seg leve)"
            },
            # Homens Idosos - Condicionamento Físico
            {
                'profile': 'homem_idoso',
                'level': 'iniciante',
                'goal': 'Condicionamento Físico',
                'description': "Baixa Intensidade: Caminhada Rápida ou Caminhada na Esteira – 15 minutos, Agachamento Assistido (com apoio de cadeira ou barra) – 3 séries de 8 a 10, Flexões de Braço (apoio de joelhos) – 3 séries de 6 a 8, Remada Baixa na Polia (carga leve) – 3 séries de 8 a 10, Abdominais (crunches) – 3 séries de 8 a 10, Bicicleta Ergométrica – 10 minutos em ritmo moderado"
            },
            {
                'profile': 'homem_idoso',
                'level': 'intermediario',
                'goal': 'Condicionamento Físico',
                'description': "Moderada Intensidade: Caminhada Rápida ou Corrida Leve – 20 minutos, Agachamento com Halteres (carga leve) – 4 séries de 10, Flexões de Braço (normais) – 4 séries de 8 a 10, Remada Unilateral com Halteres – 4 séries de 8 a 10, Abdominais (prancha) – 4 séries de 20 a 30 segundos, Bicicleta Ergométrica (HIIT) – 15 minutos (30 seg forte / 30 seg leve)"
            },
            {
                'profile': 'homem_idoso',
                'level': 'avancado',
                'goal': 'Condicionamento Físico',
                'description': "Alta Intensidade Controlada: Corrida Leve ou Intercalada (sprints) – 20 minutos (alternar 1 min rápido / 2 min leve), Agachamento com Barra (carga leve a moderada) – 5 séries de 8, Flexões de Braço (normais ou com variação, como flexões declinadas) – 5 séries de 10, Remada Curvada com Barra (carga moderada) – 5 séries de 8, Abdominais (prancha com elevação de pernas) – 5 séries de 30 segundos, Bicicleta Ergométrica (HIIT) – 20 minutos (30 seg forte / 30 seg leve)"
            },
            # Mulheres Adultas - Condicionamento Físico
            {
                'profile': 'mulher_adulta',
                'level': 'iniciante',
                'goal': 'Condicionamento Físico',
                'description': "Baixa Intensidade: Caminhada Rápida ou Caminhada na Esteira – 20 minutos, Agachamento Livre (peso corporal) – 3 séries de 12, Flexões de Braço (apoio de joelhos, se necessário) – 3 séries de 8 a 12, Remada Baixa na Polia (carga leve) – 3 séries de 10, Abdominais (crunches) – 3 séries de 12, Bicicleta Ergométrica – 10 minutos em intensidade moderada"
            },
            {
                'profile': 'mulher_adulta',
                'level': 'intermediario',
                'goal': 'Condicionamento Físico',
                'description': "Moderada Intensidade: Corrida Leve ou Caminhada rápida – 20 minutos, Agachamento com Halteres – 4 séries de 10, Flexões de Braço (normais) – 4 séries de 10 a 15, Remada Unilateral com Halteres – 4 séries de 10, Abdominais (prancha) – 4 séries de 30 segundos, Bicicleta Ergométrica (HIIT) – 15 minutos (30 seg forte / 30 seg leve)"
            },
            {
                'profile': 'mulher_adulta',
                'level': 'avancado',
                'goal': 'Condicionamento Físico',
                'description': "Alta Intensidade: Corrida Intercalada (sprints) – 25 minutos (alternar entre 1 min rápido / 2 min leve), Agachamento com Barra – 5 séries de 8 (carga moderada a pesada), Flexões de Braço (com aumento de intensidade, como flexões declinadas) – 5 séries de 12, Remada Curvada com Barra – 5 séries de 8 a 10 (carga moderada a pesada), Abdominais (prancha com elevação de pernas) – 5 séries de 45 segundos, Bicicleta Ergométrica (HIIT) – 20 minutos (30 seg forte / 30 seg leve)"
            },
            # Mulheres Idosas - Condicionamento Físico
            {
                'profile': 'mulher_idosa',
                'level': 'iniciante',
                'goal': 'Condicionamento Físico',
                'description': "Baixa Intensidade: Caminhada Rápida ou Caminhada na Esteira – 15 minutos, Agachamento Assistido (com apoio de cadeira ou barra) – 3 séries de 8 a 10, Flexões de Braço (apoio de joelhos) – 3 séries de 6 a 8, Remada Baixa na Polia (carga leve) – 3 séries de 8 a 10, Abdominais (crunches) – 3 séries de 8 a 10, Bicicleta Ergométrica – 10 minutos em ritmo moderado"
            },
            {
                'profile': 'mulher_idosa',
                'level': 'intermediario',
                'goal': 'Condicionamento Físico',
                'description': "Moderada Intensidade: Caminhada Rápida ou Corrida Leve – 20 minutos, Agachamento com Halteres (carga leve) – 4 séries de 10, Flexões de Braço (normais) – 4 séries de 8 a 10, Remada Unilateral com Halteres – 4 séries de 8 a 10, Abdominais (prancha) – 4 séries de 20 a 30 segundos, Bicicleta Ergométrica (HIIT) – 15 minutos (30 seg forte / 30 seg leve)"
            },
            {
                'profile': 'mulher_idosa',
                'level': 'avancado',
                'goal': 'Condicionamento Físico',
                'description': "Alta Intensidade Controlada: Corrida Leve ou Intercalada (sprints) – 20 minutos (alternar entre 1 min rápido / 2 min leve), Agachamento com Barra (carga leve a moderada) – 5 séries de 8, Flexões de Braço (normais ou com variação, como flexões declinadas) – 5 séries de 10, Remada Curvada com Barra (carga moderada) – 5 séries de 8, Abdominais (prancha com elevação de pernas) – 5 séries de 30 segundos, Bicicleta Ergométrica (HIIT) – 20 minutos (30 seg forte / 30 seg leve)"
            },

        ]

        for training in trainings:
            PredefinedTraining.objects.update_or_create(
                profile=training['profile'],
                level=training['level'],
                goal=training['goal'],
                defaults={'description': training['description']}
            )

        self.stdout.write(self.style.SUCCESS('Treinos pré-determinados populados com sucesso!'))
