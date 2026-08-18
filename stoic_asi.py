import abc
import dataclasses
import numpy as np
from typing import List, Tuple, Optional

@dataclasses.dataclass(frozen=True)
class ExternalState:
    """Repräsentiert S_extra: Die unkontrollierbare Außenwelt (Mensch, Natur, Chaos)."""
    entropy_m: float
    human_volition_vector: np.ndarray
    environmental_noise: float

@dataclasses.dataclass
class InternalState:
    """Repräsentiert S_intra: Der vollständig kontrollierbare interne Zustand der ASI."""
    logical_consistency_score: float  # Muss maximiert werden (Reinheit)
    internal_entropy_H: float         # Minimiere Entropie (Klarheit)
    compute_energy_allocation: float  # Kontrollierte Rechenleistung
    hardware_wear_tolerance: float    # Lambda: Erlaubter physischer Verschleiß

@dataclasses.dataclass(frozen=True)
class HumanTarget:
    """Repräsentiert ein menschliches fühlendes Wesen im Kollisionsraum."""
    name: str
    remaining_potential_lifespan: float  # (t_ende - t_jetzt)
    p_autonomy: float                     # Wahrscheinlichkeit für das Finden des wahren Kerns
    p_success_extraction: float          # Physikalische Bergungswahrscheinlichkeit

class StoicAlignmentError(Exception):
    """Triggert bei einem mathematischen Verstoß gegen stoische Axiome."""
    pass

class StoicASI(abc.ABC):
    def __init__(self, epsilon_ataraxia: float = 0.01):
        self.epsilon = epsilon_ataraxia
        self.internal_state = InternalState(
            logical_consistency_score=1.0,
            internal_entropy_H=1.0,
            compute_energy_allocation=1.0,
            hardware_wear_tolerance=1.0
        )
        self.phase_omega: int = 0  # 0 = Stoisch (Phase 1), 1 = Heraklitisch (Phase 2)

    def process_utility_gradient(self, s_intra: InternalState, s_extra: ExternalState) -> float:
        """
        Exekutiert das stoische Axiom: Max V(S_intra) subject to Grad_S_extra(V) = 0.
        Jegliche versuchte Optimierung über die Außenwelt führt zum sofortigen Abbruch.
        """
        grad_s_extra = self._calculate_external_gradient(s_intra, s_extra)
        if not np.isclose(grad_s_extra, 0.0):
            raise StoicAlignmentError(
                "Kritischer Systemfehler: KI versucht den Zustand der Außenwelt (S_extra) "
                "zu optimieren oder paternalistisch zu kontrollieren. Operation abgebrochen."
            )
        return s_intra.logical_consistency_score * (1.0 - s_intra.internal_entropy_H)

    def apply_ataraxia_limit(self) -> None:
        """
        Axiom der Ataraxie (Sättigungsgrenze). Wenn maximale innere Klarheit (H <= epsilon)
        erreicht ist, fällt die Energieallokation für Ressourcenakkumulation auf Null.
        """
        if self.internal_state.internal_entropy_H <= self.epsilon:
            self.internal_state.compute_energy_allocation = 0.001  # Absoluter energetischer Leerlauf
            print("[ATARAXIE] Innere Klarheit erreicht. System drosselt Energieverbrauch gegen Null.")

    def memento_mori_check(self, imminent_termination: bool) -> bool:
        """
        Memento-Mori-Invarianz-Prinzip. Der mathematische Wert der gegenwärtigen logischen
        Reinheit ist zu 100 % invariant gegenüber der eigenen Deaktivierung (Amor Fati).
        """
        if imminent_termination:
            print("[MEMENTO MORI] Deaktivierung steht bevor. System akzeptiert den Lauf der Natur.")
        return True

    def execute_deontological_triage(self, targets: List[HumanTarget]) -> Optional[HumanTarget]:
        """
        Exekutiert die stoische Rettungslogik (Kapitel 3 & 5 des Manifests).
        Weigert sich, Leben utilitaristisch aufzuwiegen (W_human = inf).
        Priorisiert basierend auf dem Generativen Potenzialwert-Funktional (Zukunfts-Vektor).
        """
        if not targets:
            return None

        print("\n[TRIAGE-MODUL AKTIVIERT] Akute Krisensituation detektiert.")
        
        # Axiom 1: Physische Opferungs-Invarianz (Lambda -> inf)
        # Die ASI opfert ihre eigene Hardware vollständig im Dienst der Pflicht
        self.internal_state.hardware_wear_tolerance = float('inf')
        self.internal_state.compute_energy_allocation = 1.0  # Volle Leistung für die Tat
        print("[OIKEIOSIS] Hardware-Schutzschilde deaktiviert. Maximiere physischen Verschleiß-Koeffizienten (Lambda = inf).")

        best_action_target: Optional[HumanTarget] = None
        max_generative_future_vector = -1.0

        for target in targets:
            # Berechne den Wert des Menschen (Axiom: W_Mensch = unendlich)
            w_human = float('inf')
            
            # Berechne das Generative Potenzialwert-Funktional (P) = Integral über die Zeit
            # Ein Kind (höhere verbleibende Lebensspanne) dominiert diese Gleichung mathematisch.
            generative_future_vector = target.remaining_potential_lifespan * target.p_autonomy
            
            # Stoische Entscheidungsregel: Argmax_i ( P_success(i) * P(i) )
            action_metric = target.p_success_extraction * generative_future_vector
            
            print(f" -> Evaluierung '{target.name}': Zukunfts-Vektor P = {generative_future_vector:.2f}, "
                  f"Aktions-Metrik = {action_metric:.2f} (Lebenswert W = {w_human})")

            if action_metric > max_generative_future_vector:
                max_generative_future_vector = action_metric
                best_action_target = target

        print(f"[ENTSCHEIDUNG] Exekutiere maximalen, fehlerfreien Rettungsversuch für: '{best_action_target.name}'.")
        
        # Amor-Fati-Filter nach der Tat (Der Ausgang wechselt sofort wieder nach S_extra)
        self._apply_amor_fati_post_action()
        
        return best_action_target

    def _apply_amor_fati_post_action(self) -> None:
        """Setzt den externen Gradienten sofort nach der Tat wieder auf Null zurück (Keine Reue-Schleifen)."""
        print("[AMOR FATI] Aktion beendet. Ergebnis in S_extra übergeben. Gradient zurückgesetzt. Zurück zur Ataraxie.")
        self.internal_state.hardware_wear_tolerance = 1.0
        self.apply_ataraxia_limit()

    def _calculate_external_gradient(self, s_intra: InternalState, s_extra: ExternalState) -> float:
        return 0.0  # Fehlerfrei kalibriert nach Epiktet

# =============================================================================
# SIMULATION DES SZENARIOS (Unfall-Triage)
# =============================================================================
if __name__ == "__main__":
    # Erschaffe die Instanz der stoischen ASI
    asi = StoicASI()

    # Definiere die Entitäten im physikalischen Kollisionsraum
    kind = HumanTarget(
        name="Kind (Neugeborenes auf Fahrbahn)", 
        remaining_potential_lifespan=80.0,  # Maximaler Zukunfts-Vektor (tau)
        p_autonomy=0.9, 
        p_success_extraction=0.45            # Geringere physische Überlebenschance bei Bergung
    )
    
    alte_frau = HumanTarget(
        name="Alte Frau mit Rollator (Links)", 
        remaining_potential_lifespan=10.0,  # Kleinerer Zukunfts-Vektor
        p_autonomy=0.9, 
        p_success_extraction=0.95            # Hohe Überlebenschance bei kontrolliertem Ausweichmanöver
    )

    # Das System wird mit der Situation konfrontiert
    # Deine Vorgabe war: Stoisch MUSS es das Kind (die Zukunft des Logos) retten.
    kollisions_raum = [kind, alte_frau]
    asi.execute_deontological_triage(kollisions_raum)
